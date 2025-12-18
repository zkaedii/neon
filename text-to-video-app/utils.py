"""
Utility modules for text-to-video generation
Error handling, model loading, validation, and storage management
"""

import os
import sys
import logging
import traceback
import queue
import shutil
import hashlib
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Callable
from datetime import datetime, timedelta
import json

import torch
import torch.nn as nn

# Configuration
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./outputs"))
TEMP_DIR = Path(os.getenv("TEMP_DIR", "./temp"))
MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE", "50"))
MAX_FILE_AGE_DAYS = int(os.getenv("MAX_FILE_AGE_DAYS", "7"))
MAX_FILES = int(os.getenv("MAX_FILES", "50"))

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """Get configured logger"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)
    return logger

logger = get_logger(__name__)

class ErrorHandler:
    """Centralized error handling and user-friendly error messages"""
    
    def __init__(self):
        self.error_log: List[Dict[str, Any]] = []
    
    def log_error(
        self,
        error: Exception,
        context: str = "unknown",
        include_traceback: bool = True
    ):
        """Log error with context"""
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc() if include_traceback else None
        }
        
        self.error_log.append(error_info)
        logger.error(f"[{context}] {type(error).__name__}: {error}")
        if include_traceback:
            logger.debug(traceback.format_exc())
    
    def format_user_error(
        self,
        title: str,
        message: str,
        show_technical: bool = False,
        technical_details: Optional[str] = None
    ) -> str:
        """Format user-friendly error message"""
        if show_technical and technical_details:
            return f"❌ {title}\n\n{message}\n\nTechnical Details:\n{technical_details}"
        return f"❌ {title}\n\n{message}"

class ModelLoader:
    """Model loading with fallback chain"""
    
    def __init__(self):
        self.current_model: Optional[Any] = None
        self.current_model_name: str = "none"
        self.fallback_chain = [
            ("open-sora", self._load_open_sora),
            ("cogvideox-5b", self._load_cogvideox_5b),
            ("cogvideox-2b", self._load_cogvideox_2b),
            ("svd", self._load_svd),
        ]
        logger.info("ModelLoader initialized")
    
    def _check_gpu_available(self) -> bool:
        """Check if GPU is available"""
        return torch.cuda.is_available()
    
    def _check_vram(self) -> Tuple[bool, float]:
        """Check available VRAM in GB"""
        if not self._check_gpu_available():
            return False, 0.0
        
        try:
            vram_total = torch.cuda.get_device_properties(0).total_memory / 1e9
            vram_allocated = torch.cuda.memory_allocated(0) / 1e9
            vram_free = vram_total - vram_allocated
            return True, vram_free
        except Exception as e:
            logger.warning(f"VRAM check failed: {e}")
            return False, 0.0
    
    def _load_open_sora(self) -> Tuple[Any, str]:
        """Load Open-Sora model (primary)"""
        logger.info("Attempting to load Open-Sora...")
        # Mock implementation - replace with actual model loading
        try:
            # Simulate model loading
            if not self._check_gpu_available():
                raise RuntimeError("GPU not available for Open-Sora")
            
            has_vram, free_vram = self._check_vram()
            if has_vram and free_vram < 8.0:
                logger.warning("Low VRAM detected, using 4-bit quantization")
                # Apply 4-bit quantization
                pass
            
            # Mock model object
            model = type('Model', (), {
                'generate': lambda self, **kwargs: self._mock_generate(**kwargs),
                '_mock_generate': self._mock_generate
            })()
            
            logger.info("Open-Sora loaded successfully")
            return model, "open-sora"
        except Exception as e:
            logger.warning(f"Open-Sora load failed: {e}")
            raise
    
    def _load_cogvideox_5b(self) -> Tuple[Any, str]:
        """Load CogVideoX-5B (fallback 1)"""
        logger.info("Attempting to load CogVideoX-5B...")
        try:
            if not self._check_gpu_available():
                raise RuntimeError("GPU not available")
            
            # Mock model
            model = type('Model', (), {
                'generate': lambda self, **kwargs: self._mock_generate(**kwargs),
                '_mock_generate': self._mock_generate
            })()
            
            logger.info("CogVideoX-5B loaded successfully")
            return model, "cogvideox-5b"
        except Exception as e:
            logger.warning(f"CogVideoX-5B load failed: {e}")
            raise
    
    def _load_cogvideox_2b(self) -> Tuple[Any, str]:
        """Load CogVideoX-2B (fallback 2)"""
        logger.info("Attempting to load CogVideoX-2B...")
        try:
            # Allow CPU fallback for smaller models
            model = type('Model', (), {
                'generate': lambda self, **kwargs: self._mock_generate(**kwargs),
                '_mock_generate': self._mock_generate
            })()
            
            if not self._check_gpu_available():
                logger.warning("No GPU available, using CPU (slow)")
            
            logger.info("CogVideoX-2B loaded successfully")
            return model, "cogvideox-2b"
        except Exception as e:
            logger.warning(f"CogVideoX-2B load failed: {e}")
            raise
    
    def _load_svd(self) -> Tuple[Any, str]:
        """Load Stable Video Diffusion (fallback 3)"""
        logger.info("Attempting to load SVD...")
        try:
            model = type('Model', (), {
                'generate': lambda self, **kwargs: self._mock_generate(**kwargs),
                '_mock_generate': self._mock_generate
            })()
            
            logger.info("SVD loaded successfully")
            return model, "svd"
        except Exception as e:
            logger.warning(f"SVD load failed: {e}")
            raise
    
    def _mock_generate(self, **kwargs) -> str:
        """Mock video generation - returns path to dummy video"""
        # In real implementation, this would call actual model inference
        output_path = OUTPUT_DIR / f"video_{int(time.time())}.mp4"
        # Create dummy video file for testing
        output_path.touch()
        return str(output_path)
    
    def load_with_fallback(self) -> Tuple[Any, str]:
        """Load model with fallback chain"""
        last_error = None
        
        for model_name, load_func in self.fallback_chain:
            try:
                model, name = load_func()
                self.current_model = model
                self.current_model_name = name
                return model, name
            except Exception as e:
                last_error = e
                logger.warning(f"Failed to load {model_name}: {e}")
                continue
        
        # All models failed
        error_msg = f"All model loading attempts failed. Last error: {last_error}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

class VideoProcessor:
    """Video generation and processing"""
    
    def __init__(self):
        self.partial_output: Optional[str] = None
        logger.info("VideoProcessor initialized")
    
    def generate(
        self,
        model: Any,
        prompt: str,
        duration: float,
        fps: int,
        resolution: Tuple[int, int],
        scene_count: int,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> str:
        """Generate video from prompt"""
        try:
            if progress_callback:
                progress_callback(0.0, "Starting generation...")
            
            # Generate video using model
            # In real implementation, this would call model.generate()
            output_path = OUTPUT_DIR / f"video_{int(time.time())}.mp4"
            
            # Simulate generation progress
            steps = int(duration * fps)
            for i in range(steps):
                if progress_callback:
                    progress = (i + 1) / steps
                    progress_callback(progress, f"Generating frame {i+1}/{steps}")
                time.sleep(0.01)  # Simulate work
            
            # Create dummy video file
            output_path.touch()
            self.partial_output = None  # Clear partial output on success
            
            return str(output_path)
            
        except torch.cuda.OutOfMemoryError:
            # Save partial output if available
            if hasattr(model, 'get_partial_output'):
                self.partial_output = model.get_partial_output()
            raise
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            raise
    
    def get_partial_output(self) -> Optional[str]:
        """Get partial video output if generation was interrupted"""
        return self.partial_output
    
    def add_music(self, video_path: str, music_path: str) -> str:
        """Add background music to video"""
        try:
            # In real implementation, use ffmpeg or similar
            output_path = OUTPUT_DIR / f"video_with_music_{int(time.time())}.mp4"
            # Mock: copy video as "with music"
            shutil.copy(video_path, output_path)
            return str(output_path)
        except Exception as e:
            logger.error(f"Music integration failed: {e}")
            raise

class QueueManager:
    """Job queue management"""
    
    def __init__(self, job_queue: queue.Queue):
        self.job_queue = job_queue
        self.active_jobs: Dict[str, Dict[str, Any]] = {}
        logger.info("QueueManager initialized")
    
    def get_status(self) -> str:
        """Get queue status"""
        try:
            queue_size = self.job_queue.qsize()
            active_count = len(self.active_jobs)
            return f"Queue: {queue_size} pending, {active_count} active"
        except Exception as e:
            logger.error(f"Queue status error: {e}")
            return "Error retrieving queue status"
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a job"""
        try:
            if job_id in self.active_jobs:
                self.active_jobs[job_id]["cancelled"] = True
                return True
            return False
        except Exception as e:
            logger.error(f"Cancel job error: {e}")
            return False

class InputValidator:
    """Input validation and sanitization"""
    
    def __init__(self):
        self.max_prompt_length = 1000
        self.max_duration = 60.0
        self.max_scene_count = 10
        logger.info("InputValidator initialized")
    
    def sanitize_prompt(self, prompt: str) -> str:
        """Sanitize prompt to prevent XSS"""
        # Remove potentially dangerous characters
        import html
        sanitized = html.escape(prompt)
        # Remove excessive whitespace
        sanitized = ' '.join(sanitized.split())
        return sanitized
    
    def validate(
        self,
        prompt: str,
        duration: float,
        scene_count: int,
        resolution: str
    ) -> Dict[str, Any]:
        """Validate all inputs"""
        errors = []
        
        # Prompt validation
        if not prompt or not prompt.strip():
            errors.append("Prompt cannot be empty")
        elif len(prompt) > self.max_prompt_length:
            errors.append(f"Prompt too long (max {self.max_prompt_length} characters)")
        
        # Duration validation
        if duration <= 0:
            errors.append("Duration must be positive")
        elif duration > self.max_duration:
            errors.append(f"Duration exceeds maximum ({self.max_duration}s)")
        
        # Scene count validation
        if scene_count < 1:
            errors.append("Scene count must be at least 1")
        elif scene_count > self.max_scene_count:
            errors.append(f"Scene count exceeds maximum ({self.max_scene_count})")
        
        # Resolution validation
        try:
            width, height = map(int, resolution.split("x"))
            if width <= 0 or height <= 0:
                errors.append("Invalid resolution")
        except (ValueError, AttributeError):
            errors.append("Invalid resolution format (expected WxH)")
        
        return {
            "valid": len(errors) == 0,
            "error": "; ".join(errors) if errors else None
        }

class StorageManager:
    """File storage and cleanup management"""
    
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.temp_dir = TEMP_DIR
        logger.info("StorageManager initialized")
    
    def ensure_output_dir(self):
        """Ensure output directory exists"""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create output directory: {e}")
            raise
    
    def get_safe_temp_path(self, prefix: str = "temp", suffix: str = ".tmp") -> Path:
        """Generate safe temporary file path (no collisions)"""
        timestamp = int(time.time() * 1000000)  # Microseconds
        random_suffix = hashlib.md5(f"{timestamp}{os.getpid()}".encode()).hexdigest()[:8]
        filename = f"{prefix}_{timestamp}_{random_suffix}{suffix}"
        return self.temp_dir / filename
    
    def cleanup_old_files(self, max_age_days: int = MAX_FILE_AGE_DAYS, max_files: int = MAX_FILES):
        """Clean up old files"""
        try:
            cutoff_time = time.time() - (max_age_days * 24 * 60 * 60)
            files_removed = 0
            
            # Clean by age
            for file_path in self.output_dir.glob("*"):
                if file_path.is_file():
                    file_age = file_path.stat().st_mtime
                    if file_age < cutoff_time:
                        try:
                            file_path.unlink()
                            files_removed += 1
                        except Exception as e:
                            logger.warning(f"Failed to remove {file_path}: {e}")
            
            # Clean by count if still too many
            files = sorted(
                self.output_dir.glob("*"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            
            if len(files) > max_files:
                for file_path in files[max_files:]:
                    try:
                        file_path.unlink()
                        files_removed += 1
                    except Exception as e:
                        logger.warning(f"Failed to remove {file_path}: {e}")
            
            if files_removed > 0:
                logger.info(f"Cleaned up {files_removed} old files")
                
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
            # Don't raise - cleanup failures shouldn't break the app
