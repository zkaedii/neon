"""
Text-to-Video Generation Web App
Open-source, self-hosted solution with comprehensive error handling
"""

import os
import sys
import logging
import traceback
import queue
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from datetime import datetime

import gradio as gr
import torch
from PIL import Image
import numpy as np

# Import utilities
from utils import (
    ErrorHandler,
    ModelLoader,
    VideoProcessor,
    QueueManager,
    InputValidator,
    StorageManager,
    get_logger,
    DEBUG_MODE
)

# Configure logging
logger = get_logger(__name__)

# Global state
job_queue = queue.Queue(maxsize=50)  # Max 50 jobs
queue_manager = QueueManager(job_queue)
model_loader = ModelLoader()
video_processor = VideoProcessor()
storage_manager = StorageManager()
error_handler = ErrorHandler()

# Job tracking
active_jobs: Dict[str, Dict[str, Any]] = {}
job_lock = threading.Lock()

@dataclass
class GenerationJob:
    """Job data structure"""
    job_id: str
    prompt: str
    duration: float
    fps: int
    resolution: Tuple[int, int]
    music_path: Optional[str]
    scene_count: int
    timestamp: float

def generate_video(
    prompt: str,
    duration: float,
    fps: int = 24,
    resolution: str = "512x512",
    music_file: Optional[gr.File] = None,
    scene_count: int = 1,
    progress=gr.Progress()
) -> Tuple[Optional[str], Optional[str], str]:
    """
    Main video generation function with comprehensive error handling
    
    Returns: (video_path, audio_path, status_message)
    """
    try:
        # Input validation
        validator = InputValidator()
        validation_result = validator.validate(
            prompt=prompt,
            duration=duration,
            scene_count=scene_count,
            resolution=resolution
        )
        
        if not validation_result["valid"]:
            error_msg = error_handler.format_user_error(
                "Validation Error",
                validation_result["error"],
                show_technical=False
            )
            return None, None, error_msg
        
        # Generate job ID
        job_id = f"job_{int(time.time() * 1000)}"
        
        # Check queue capacity
        if job_queue.full():
            error_msg = error_handler.format_user_error(
                "Queue Full",
                "Maximum queue size reached. Please try again later.",
                show_technical=False
            )
            return None, None, error_msg
        
        # Create job
        width, height = map(int, resolution.split("x"))
        job = GenerationJob(
            job_id=job_id,
            prompt=prompt,
            duration=duration,
            fps=fps,
            resolution=(width, height),
            music_path=music_file.name if music_file else None,
            scene_count=scene_count,
            timestamp=time.time()
        )
        
        # Add to queue
        try:
            job_queue.put_nowait(job)
        except queue.Full:
            error_msg = error_handler.format_user_error(
                "Queue Full",
                "Could not add job to queue. Please try again.",
                show_technical=False
            )
            return None, None, error_msg
        
        # Process job
        progress(0, desc="Initializing model...")
        
        try:
            # Load model with fallback
            model, model_name = model_loader.load_with_fallback()
            progress(0.1, desc=f"Using model: {model_name}")
            
            # Process video generation
            progress(0.2, desc="Generating video frames...")
            
            video_path = video_processor.generate(
                model=model,
                prompt=prompt,
                duration=duration,
                fps=fps,
                resolution=(width, height),
                scene_count=scene_count,
                progress_callback=lambda p, msg: progress(0.2 + p * 0.7, desc=msg)
            )
            
            progress(0.9, desc="Finalizing video...")
            
            # Handle music integration
            audio_path = None
            if music_file and os.path.exists(music_file.name):
                try:
                    audio_path = video_processor.add_music(
                        video_path=video_path,
                        music_path=music_file.name
                    )
                    final_video = audio_path
                except Exception as e:
                    logger.warning(f"Music integration failed: {e}")
                    error_handler.log_error(e, context="music_integration")
                    final_video = video_path
            else:
                final_video = video_path
            
            progress(1.0, desc="Complete!")
            
            # Cleanup old files
            storage_manager.cleanup_old_files()
            
            status_msg = f"✅ Video generated successfully using {model_name}"
            return final_video, audio_path, status_msg
            
        except torch.cuda.OutOfMemoryError as e:
            error_handler.log_error(e, context="oom_error")
            # Try to save partial video if exists
            partial_video = video_processor.get_partial_output()
            if partial_video:
                error_msg = error_handler.format_user_error(
                    "Out of Memory",
                    "Video generation ran out of GPU memory. A partial video was saved.",
                    show_technical=True,
                    technical_details=str(e)
                )
                return partial_video, None, error_msg
            else:
                error_msg = error_handler.format_user_error(
                    "Out of Memory",
                    "Video generation requires more GPU memory. Try reducing resolution or duration.",
                    show_technical=True,
                    technical_details=str(e)
                )
                return None, None, error_msg
                
        except RuntimeError as e:
            error_handler.log_error(e, context="runtime_error")
            error_msg = error_handler.format_user_error(
                "Generation Error",
                "An error occurred during video generation. You can retry.",
                show_technical=True,
                technical_details=str(e)
            )
            return None, None, error_msg
            
        except TimeoutError as e:
            error_handler.log_error(e, context="timeout_error")
            error_msg = error_handler.format_user_error(
                "Timeout",
                "Video generation timed out. The job has been cancelled.",
                show_technical=True,
                technical_details=str(e)
            )
            return None, None, error_msg
            
        except Exception as e:
            error_handler.log_error(e, context="unexpected_error")
            error_msg = error_handler.format_user_error(
                "Unexpected Error",
                "An unexpected error occurred. Please check the logs.",
                show_technical=DEBUG_MODE,
                technical_details=traceback.format_exc()
            )
            return None, None, error_msg
        
        finally:
            # Cleanup job tracking
            with job_lock:
                if job_id in active_jobs:
                    del active_jobs[job_id]
    
    except Exception as e:
        error_handler.log_error(e, context="top_level_error")
        error_msg = error_handler.format_user_error(
            "System Error",
            "A system error occurred. Please try again.",
            show_technical=DEBUG_MODE,
            technical_details=traceback.format_exc()
        )
        return None, None, error_msg

def get_queue_status() -> str:
    """Get current queue status"""
    try:
        return queue_manager.get_status()
    except Exception as e:
        error_handler.log_error(e, context="queue_status")
        return "Error retrieving queue status"

def cancel_job(job_id: str) -> str:
    """Cancel a specific job"""
    try:
        result = queue_manager.cancel_job(job_id)
        if result:
            return f"Job {job_id} cancelled successfully"
        else:
            return f"Job {job_id} not found or already completed"
    except Exception as e:
        error_handler.log_error(e, context="cancel_job")
        return f"Error cancelling job: {str(e)}"

# Gradio Interface
def create_interface():
    """Create and configure Gradio interface"""
    
    with gr.Blocks(title="Text-to-Video Generator", theme=gr.themes.Soft()) as app:
        gr.Markdown("# 🎬 Open-Source Text-to-Video Generator")
        gr.Markdown("Generate videos from text prompts using open-source models")
        
        with gr.Row():
            with gr.Column(scale=2):
                prompt_input = gr.Textbox(
                    label="Prompt",
                    placeholder="A beautiful sunset over the ocean with waves crashing...",
                    lines=3,
                    max_lines=5
                )
                
                with gr.Row():
                    duration_input = gr.Slider(
                        label="Duration (seconds)",
                        minimum=1.0,
                        maximum=60.0,
                        value=5.0,
                        step=0.5
                    )
                    fps_input = gr.Slider(
                        label="FPS",
                        minimum=12,
                        maximum=30,
                        value=24,
                        step=1
                    )
                
                with gr.Row():
                    resolution_input = gr.Dropdown(
                        label="Resolution",
                        choices=["256x256", "512x512", "768x768", "1024x1024"],
                        value="512x512"
                    )
                    scene_count_input = gr.Slider(
                        label="Scene Count",
                        minimum=1,
                        maximum=10,
                        value=1,
                        step=1
                    )
                
                music_input = gr.File(
                    label="Background Music (Optional)",
                    file_types=["audio"]
                )
                
                generate_btn = gr.Button("Generate Video", variant="primary")
            
            with gr.Column(scale=1):
                gr.Markdown("### Queue Status")
                queue_status = gr.Textbox(
                    label="Status",
                    value="Ready",
                    interactive=False
                )
                refresh_queue_btn = gr.Button("Refresh Status")
        
        with gr.Row():
            video_output = gr.Video(label="Generated Video")
            status_output = gr.Textbox(
                label="Status",
                interactive=False,
                lines=5
            )
        
        # Event handlers
        generate_btn.click(
            fn=generate_video,
            inputs=[
                prompt_input,
                duration_input,
                fps_input,
                resolution_input,
                music_input,
                scene_count_input
            ],
            outputs=[video_output, gr.File(label="Audio"), status_output]
        )
        
        refresh_queue_btn.click(
            fn=get_queue_status,
            inputs=None,
            outputs=queue_status
        )
        
        # Auto-refresh queue status
        app.load(
            fn=get_queue_status,
            inputs=None,
            outputs=queue_status,
            every=5
        )
    
    return app

def main():
    """Main entry point"""
    try:
        # Initialize components
        logger.info("Initializing Text-to-Video Generator...")
        
        # Create output directory
        storage_manager.ensure_output_dir()
        
        # Pre-load model (optional, can be lazy-loaded)
        logger.info("Pre-loading model...")
        try:
            model_loader.load_with_fallback()
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.warning(f"Model pre-load failed (will load on first generation): {e}")
        
        # Create and launch interface
        app = create_interface()
        app.launch(
            server_name="0.0.0.0",
            server_port=int(os.getenv("PORT", 7860)),
            share=os.getenv("GRADIO_SHARE", "False").lower() == "true"
        )
        
    except Exception as e:
        error_handler.log_error(e, context="main_initialization")
        logger.critical(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
