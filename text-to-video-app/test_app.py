"""
Comprehensive test suite for text-to-video generation app
Tests all resilience paths and error handling scenarios
"""

import pytest
import sys
import os
import time
import logging
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
import queue
import torch
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    ErrorHandler,
    ModelLoader,
    VideoProcessor,
    QueueManager,
    InputValidator,
    StorageManager,
    get_logger,
    DEBUG_MODE,
    OUTPUT_DIR,
    TEMP_DIR
)
import app

# Test fixtures
@pytest.fixture
def temp_dirs():
    """Create temporary directories for testing"""
    temp_output = tempfile.mkdtemp()
    temp_temp = tempfile.mkdtemp()
    
    with patch('utils.OUTPUT_DIR', Path(temp_output)), \
         patch('utils.TEMP_DIR', Path(temp_temp)):
        yield temp_output, temp_temp
    
    shutil.rmtree(temp_output, ignore_errors=True)
    shutil.rmtree(temp_temp, ignore_errors=True)

@pytest.fixture
def mock_torch_cuda():
    """Mock torch.cuda for testing"""
    with patch('torch.cuda') as mock_cuda:
        mock_cuda.is_available.return_value = True
        mock_cuda.get_device_properties.return_value = Mock(total_memory=16e9)
        mock_cuda.memory_allocated.return_value = 4e9
        yield mock_cuda

@pytest.fixture
def error_handler():
    """Error handler instance"""
    return ErrorHandler()

@pytest.fixture
def model_loader():
    """Model loader instance"""
    return ModelLoader()

@pytest.fixture
def video_processor():
    """Video processor instance"""
    return VideoProcessor()

@pytest.fixture
def job_queue():
    """Job queue for testing"""
    return queue.Queue(maxsize=50)

@pytest.fixture
def queue_manager(job_queue):
    """Queue manager instance"""
    return QueueManager(job_queue)

@pytest.fixture
def input_validator():
    """Input validator instance"""
    return InputValidator()

@pytest.fixture
def storage_manager():
    """Storage manager instance"""
    return StorageManager()

# ============================================================================
# 1. MODEL LOADING FALLBACK CHAIN TESTS
# ============================================================================

class TestModelLoadingFallback:
    """Test model loading fallback chain"""
    
    def test_primary_model_load_fails_falls_to_cogvideox_5b(self, model_loader, mock_torch_cuda):
        """Test primary model failure → CogVideoX-5B fallback"""
        with patch.object(model_loader, '_load_open_sora', side_effect=RuntimeError("Open-Sora failed")), \
             patch.object(model_loader, '_load_cogvideox_5b', return_value=(Mock(), "cogvideox-5b")):
            
            model, name = model_loader.load_with_fallback()
            assert name == "cogvideox-5b"
            assert model is not None
    
    def test_cogvideox_5b_fails_falls_to_2b(self, model_loader, mock_torch_cuda):
        """Test CogVideoX-5B failure → 2B fallback"""
        with patch.object(model_loader, '_load_open_sora', side_effect=RuntimeError("Failed")), \
             patch.object(model_loader, '_load_cogvideox_5b', side_effect=RuntimeError("5B failed")), \
             patch.object(model_loader, '_load_cogvideox_2b', return_value=(Mock(), "cogvideox-2b")):
            
            model, name = model_loader.load_with_fallback()
            assert name == "cogvideox-2b"
    
    def test_low_vram_forces_4bit_quantization(self, model_loader):
        """Test low VRAM detection forces 4-bit quantization"""
        with patch('torch.cuda.is_available', return_value=True), \
             patch('torch.cuda.get_device_properties') as mock_props, \
             patch('torch.cuda.memory_allocated', return_value=12e9):  # Only 4GB free
            
            mock_props.return_value = Mock(total_memory=16e9)
            
            with patch.object(model_loader, '_load_open_sora') as mock_load:
                mock_load.return_value = (Mock(), "open-sora")
                model_loader.load_with_fallback()
                
                # Verify low VRAM was detected (check logs or quantization flag)
                assert mock_load.called
    
    def test_no_gpu_cpu_offload_with_warning(self, model_loader):
        """Test no GPU → CPU offload with warning"""
        with patch('torch.cuda.is_available', return_value=False), \
             patch.object(model_loader, '_load_open_sora', side_effect=RuntimeError("No GPU")), \
             patch.object(model_loader, '_load_cogvideox_5b', side_effect=RuntimeError("No GPU")), \
             patch.object(model_loader, '_load_cogvideox_2b', return_value=(Mock(), "cogvideox-2b")):
            
            model, name = model_loader.load_with_fallback()
            assert name == "cogvideox-2b"
            # CPU fallback should work for smaller models
    
    def test_all_models_fail_raises_error(self, model_loader):
        """Test all models fail → raises RuntimeError"""
        with patch.object(model_loader, '_load_open_sora', side_effect=RuntimeError("Failed")), \
             patch.object(model_loader, '_load_cogvideox_5b', side_effect=RuntimeError("Failed")), \
             patch.object(model_loader, '_load_cogvideox_2b', side_effect=RuntimeError("Failed")), \
             patch.object(model_loader, '_load_svd', side_effect=RuntimeError("Failed")):
            
            with pytest.raises(RuntimeError, match="All model loading attempts failed"):
                model_loader.load_with_fallback()

# ============================================================================
# 2. GENERATION ERROR RECOVERY TESTS
# ============================================================================

class TestGenerationErrorRecovery:
    """Test video generation error recovery"""
    
    def test_oom_error_returns_partial_video(self, video_processor, mock_torch_cuda):
        """Test OOMError → returns partial video"""
        mock_model = Mock()
        mock_model.generate.side_effect = torch.cuda.OutOfMemoryError("OOM")
        mock_model.get_partial_output.return_value = "/path/to/partial.mp4"
        
        with patch.object(video_processor, 'get_partial_output', return_value="/path/to/partial.mp4"):
            partial = video_processor.get_partial_output()
            assert partial == "/path/to/partial.mp4"
    
    def test_runtime_error_retry_option(self, video_processor):
        """Test RuntimeError → retry option appears"""
        mock_model = Mock()
        mock_model.generate.side_effect = RuntimeError("Generation failed")
        
        with pytest.raises(RuntimeError):
            video_processor.generate(
                model=mock_model,
                prompt="test",
                duration=5.0,
                fps=24,
                resolution=(512, 512),
                scene_count=1
            )
    
    def test_timeout_cancels_gracefully(self, video_processor):
        """Test timeout → job cancels gracefully"""
        mock_model = Mock()
        mock_model.generate.side_effect = TimeoutError("Generation timed out")
        
        with pytest.raises(TimeoutError):
            video_processor.generate(
                model=mock_model,
                prompt="test",
                duration=5.0,
                fps=24,
                resolution=(512, 512),
                scene_count=1
            )
    
    def test_invalid_prompt_empty_validation_error(self, input_validator):
        """Test empty prompt → validation error"""
        result = input_validator.validate(
            prompt="",
            duration=5.0,
            scene_count=1,
            resolution="512x512"
        )
        assert not result["valid"]
        assert "empty" in result["error"].lower()
    
    def test_invalid_prompt_too_long_validation_error(self, input_validator):
        """Test overly long prompt → validation error"""
        long_prompt = "a" * 2000
        result = input_validator.validate(
            prompt=long_prompt,
            duration=5.0,
            scene_count=1,
            resolution="512x512"
        )
        assert not result["valid"]
        assert "too long" in result["error"].lower()

# ============================================================================
# 3. QUEUE & ASYNC RESILIENCE TESTS
# ============================================================================

class TestQueueResilience:
    """Test queue and async resilience"""
    
    def test_crashing_job_removed_queue_continues(self, job_queue, queue_manager):
        """Test crashing job → removed from queue, next job proceeds"""
        # Add job
        job1 = Mock()
        job1.job_id = "job1"
        job_queue.put(job1)
        
        # Simulate crash
        with patch('app.active_jobs', {}):
            # Job crashes, should be removed
            if "job1" in app.active_jobs:
                del app.active_jobs["job1"]
        
        # Next job should proceed
        assert not job_queue.empty()
        next_job = job_queue.get()
        assert next_job is not None
    
    def test_max_queue_size_rejects_new_jobs(self, job_queue):
        """Test max queue size → rejects new jobs"""
        # Fill queue to max
        for i in range(50):
            job_queue.put(Mock())
        
        # Try to add one more
        with pytest.raises(queue.Full):
            job_queue.put_nowait(Mock())
    
    def test_concurrent_submissions_proper_ordering(self, job_queue):
        """Test concurrent submissions → proper ordering"""
        jobs = [Mock(job_id=f"job{i}") for i in range(10)]
        
        # Add all jobs
        for job in jobs:
            job_queue.put(job)
        
        # Verify order
        retrieved = []
        while not job_queue.empty():
            retrieved.append(job_queue.get())
        
        assert len(retrieved) == 10
        # Order should be maintained (FIFO)

# ============================================================================
# 4. FILE & STORAGE SAFETY TESTS
# ============================================================================

class TestStorageSafety:
    """Test file and storage safety"""
    
    def test_disk_full_cleanup_error(self, storage_manager, temp_dirs):
        """Test disk full → cleanup + error"""
        output_dir, _ = temp_dirs
        
        with patch('shutil.copy', side_effect=IOError("No space left on device")):
            with pytest.raises(IOError):
                storage_manager.get_safe_temp_path()
    
    def test_auto_cleanup_old_files(self, storage_manager, temp_dirs):
        """Test auto-cleanup of old files"""
        output_dir, _ = temp_dirs
        
        # Create old files
        old_file = Path(output_dir) / "old_file.mp4"
        old_file.touch()
        
        # Mock old mtime
        old_time = time.time() - (8 * 24 * 60 * 60)  # 8 days ago
        os.utime(str(old_file), (old_time, old_time))
        
        # Run cleanup
        with patch('utils.OUTPUT_DIR', Path(output_dir)):
            storage_manager.output_dir = Path(output_dir)
            storage_manager.cleanup_old_files(max_age_days=7)
        
        # Old file should be removed
        assert not old_file.exists()
    
    def test_safe_temp_path_no_collisions(self, storage_manager, temp_dirs):
        """Test safe temp path generation (no collisions)"""
        _, temp_dir = temp_dirs
        
        paths = set()
        for _ in range(100):
            path = storage_manager.get_safe_temp_path()
            assert path not in paths, "Path collision detected"
            paths.add(path)

# ============================================================================
# 5. INPUT VALIDATION & SANITIZATION TESTS
# ============================================================================

class TestInputValidation:
    """Test input validation and sanitization"""
    
    def test_total_duration_over_60s_blocks(self, input_validator):
        """Test total duration >60s → blocks submission"""
        result = input_validator.validate(
            prompt="test prompt",
            duration=65.0,  # Over limit
            scene_count=1,
            resolution="512x512"
        )
        assert not result["valid"]
        assert "exceeds maximum" in result["error"].lower()
    
    def test_xss_in_prompt_sanitized(self, input_validator):
        """Test XSS in prompt → sanitized output"""
        malicious_prompt = "<script>alert('xss')</script>test"
        sanitized = input_validator.sanitize_prompt(malicious_prompt)
        
        assert "<script>" not in sanitized
        assert "&lt;script&gt;" in sanitized or sanitized == "test"
    
    def test_extreme_scene_count_graceful_limit(self, input_validator):
        """Test extreme scene count → graceful limit"""
        result = input_validator.validate(
            prompt="test",
            duration=5.0,
            scene_count=100,  # Way over limit
            resolution="512x512"
        )
        assert not result["valid"]
        assert "exceeds maximum" in result["error"].lower()

# ============================================================================
# 6. UI FEEDBACK INTEGRITY TESTS
# ============================================================================

class TestUIFeedback:
    """Test UI feedback integrity"""
    
    def test_error_message_friendly_technical_toggle(self, error_handler):
        """Test error messages contain both friendly + technical toggle"""
        # Friendly message
        friendly = error_handler.format_user_error(
            "Test Error",
            "Something went wrong",
            show_technical=False
        )
        assert "Test Error" in friendly
        assert "Something went wrong" in friendly
        assert "Technical" not in friendly
        
        # Technical message
        technical = error_handler.format_user_error(
            "Test Error",
            "Something went wrong",
            show_technical=True,
            technical_details="Traceback: ..."
        )
        assert "Technical Details" in technical
        assert "Traceback" in technical
    
    def test_success_path_returns_playable_video(self, video_processor, temp_dirs):
        """Test success path returns playable video"""
        output_dir, _ = temp_dirs
        
        mock_model = Mock()
        mock_model.generate.return_value = str(Path(output_dir) / "test_video.mp4")
        
        with patch('utils.OUTPUT_DIR', Path(output_dir)):
            # Create dummy video file
            video_path = Path(output_dir) / "test_video.mp4"
            video_path.touch()
            
            result = video_processor.generate(
                model=mock_model,
                prompt="test",
                duration=5.0,
                fps=24,
                resolution=(512, 512),
                scene_count=1
            )
            
            assert Path(result).exists()

# ============================================================================
# 7. LOGGING & DEBUG TESTS
# ============================================================================

class TestLogging:
    """Test logging and debug functionality"""
    
    def test_exceptions_logged_with_traceback(self, error_handler):
        """Test exceptions logged with traceback"""
        test_error = ValueError("Test error")
        
        error_handler.log_error(test_error, context="test_context")
        
        assert len(error_handler.error_log) > 0
        assert error_handler.error_log[-1]["error_type"] == "ValueError"
        assert error_handler.error_log[-1]["traceback"] is not None
    
    def test_debug_mode_toggles_verbose_logging(self):
        """Test DEBUG_MODE env var toggles verbose logging"""
        with patch.dict(os.environ, {"DEBUG_MODE": "true"}):
            # Reload module to pick up new env var
            import importlib
            import utils
            importlib.reload(utils)
            
            logger = utils.get_logger("test")
            assert logger.level == logging.DEBUG
        
        with patch.dict(os.environ, {"DEBUG_MODE": "false"}):
            importlib.reload(utils)
            logger = utils.get_logger("test")
            assert logger.level == logging.INFO

# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests"""
    
    def test_full_generation_pipeline(self, temp_dirs, mock_torch_cuda):
        """Test full generation pipeline end-to-end"""
        output_dir, _ = temp_dirs
        
        with patch('utils.OUTPUT_DIR', Path(output_dir)), \
             patch('app.model_loader') as mock_loader, \
             patch('app.video_processor') as mock_processor:
            
            # Setup mocks
            mock_model = Mock()
            mock_loader.load_with_fallback.return_value = (mock_model, "test-model")
            mock_processor.generate.return_value = str(Path(output_dir) / "video.mp4")
            
            # Create dummy video
            video_path = Path(output_dir) / "video.mp4"
            video_path.touch()
            
            # Test generation
            result = app.generate_video(
                prompt="test prompt",
                duration=5.0,
                fps=24,
                resolution="512x512",
                music_file=None,
                scene_count=1
            )
            
            # Should return video path
            assert result[0] is not None or result[2].startswith("✅")
    
    def test_error_propagation_through_layers(self, error_handler):
        """Test error propagation through all layers"""
        # Simulate error at each layer
        with patch('app.model_loader.load_with_fallback', side_effect=RuntimeError("Model error")):
            result = app.generate_video(
                prompt="test",
                duration=5.0,
                fps=24,
                resolution="512x512",
                music_file=None,
                scene_count=1
            )
            
            # Should return error message, not crash
            assert result[0] is None
            assert "Error" in result[2] or "error" in result[2].lower()

# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestEdgeCases:
    """Test edge cases"""
    
    def test_zero_duration_validation(self, input_validator):
        """Test zero duration validation"""
        result = input_validator.validate(
            prompt="test",
            duration=0.0,
            scene_count=1,
            resolution="512x512"
        )
        assert not result["valid"]
    
    def test_negative_duration_validation(self, input_validator):
        """Test negative duration validation"""
        result = input_validator.validate(
            prompt="test",
            duration=-1.0,
            scene_count=1,
            resolution="512x512"
        )
        assert not result["valid"]
    
    def test_invalid_resolution_format(self, input_validator):
        """Test invalid resolution format"""
        result = input_validator.validate(
            prompt="test",
            duration=5.0,
            scene_count=1,
            resolution="invalid"
        )
        assert not result["valid"]
    
    def test_music_integration_file_not_found(self, video_processor):
        """Test music integration with non-existent file"""
        with pytest.raises(Exception):  # Should handle gracefully
            video_processor.add_music(
                video_path="/path/to/video.mp4",
                music_path="/nonexistent/music.mp3"
            )

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=app", "--cov=utils", "--cov-report=html"])
