# 🎬 Open-Source Text-to-Video Generator

A complete, self-hosted web application for generating videos from text prompts using only legal open-source models. Built with comprehensive error handling, resilience testing, and production-ready architecture.

[![Tests](https://github.com/yourusername/text-to-video-app/workflows/Tests/badge.svg)](https://github.com/yourusername/text-to-video-app/actions)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)](https://github.com/yourusername/text-to-video-app)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ✨ Features

- **Multi-Model Fallback Chain**: Automatically falls back through Open-Sora → CogVideoX-5B → CogVideoX-2B → SVD
- **Intelligent Resource Management**: Auto-detects VRAM and applies 4-bit quantization when needed
- **Music Integration**: Add background music to generated videos
- **Queue System**: Handles concurrent requests with proper job management
- **Comprehensive Error Handling**: Graceful degradation under all failure scenarios
- **Production-Ready**: Docker support, health checks, logging, and monitoring
- **Fully Tested**: 90%+ test coverage with pytest, including all error paths

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Build and run
docker build -t text-to-video-app .
docker run -p 7860:7860 --gpus all text-to-video-app

# Or build with test stage
docker build --target test -t text-to-video-app:test .
```

### Local Installation

```bash
# Clone repository
git clone https://github.com/yourusername/text-to-video-app.git
cd text-to-video-app

# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
export DEBUG_MODE=true
export OUTPUT_DIR=./outputs
export PORT=7860

# Run application
python app.py
```

Access the web interface at `http://localhost:7860`

## 📋 Requirements

- Python 3.10+
- CUDA-capable GPU (recommended) or CPU fallback
- 8GB+ VRAM for full models, 4GB+ for quantized
- Docker (optional, for containerized deployment)

## 🧪 Running Tests

### Run All Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest test_app.py -v --cov=app --cov=utils --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Run Specific Test Categories

```bash
# Model loading tests
pytest test_app.py::TestModelLoadingFallback -v

# Error recovery tests
pytest test_app.py::TestGenerationErrorRecovery -v

# Queue resilience tests
pytest test_app.py::TestQueueResilience -v

# Storage safety tests
pytest test_app.py::TestStorageSafety -v

# Integration tests
pytest test_app.py::TestIntegration -v
```

### Test Coverage Goals

- **Overall Coverage**: >90%
- **Error Handling Modules**: >95%
- **Critical Paths**: 100%

Current coverage can be viewed in `htmlcov/index.html` after running tests.

## 🏗️ Architecture

### Model Fallback Chain

```
Open-Sora (Primary)
    ↓ [Fails]
CogVideoX-5B
    ↓ [Fails]
CogVideoX-2B (CPU-capable)
    ↓ [Fails]
Stable Video Diffusion (SVD)
    ↓ [All Fail]
RuntimeError with helpful message
```

### Error Handling Strategy

1. **Model Loading**: Automatic fallback through model chain
2. **Generation Errors**: Partial video recovery, user-friendly messages
3. **Resource Errors**: Graceful degradation (4-bit quantization, CPU fallback)
4. **Queue Management**: Job cancellation, max size limits
5. **Storage Errors**: Automatic cleanup, safe temp file generation

## 📁 Project Structure

```
text-to-video-app/
├── app.py              # Main Gradio application
├── utils.py            # Error handling, model loading, validation
├── test_app.py         # Comprehensive test suite
├── requirements.txt    # Python dependencies
├── Dockerfile          # Multi-stage Docker build
├── README.md           # This file
├── .github/
│   └── workflows/
│       └── ci.yml      # GitHub Actions CI
└── outputs/            # Generated videos (created at runtime)
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG_MODE` | `false` | Enable verbose logging and technical error details |
| `OUTPUT_DIR` | `./outputs` | Directory for generated videos |
| `TEMP_DIR` | `./temp` | Temporary file directory |
| `PORT` | `7860` | Web server port |
| `MAX_QUEUE_SIZE` | `50` | Maximum concurrent jobs |
| `MAX_FILE_AGE_DAYS` | `7` | Auto-cleanup files older than this |
| `MAX_FILES` | `50` | Maximum files before cleanup |

### Model Configuration

Models are loaded automatically based on available resources:
- **High VRAM (>8GB)**: Full precision models
- **Low VRAM (4-8GB)**: 4-bit quantized models
- **No GPU**: CPU fallback (slower, smaller models only)

## 🛡️ Resilience Features

### Tested Resilience Paths

✅ **Model Loading Fallback Chain**
- Primary model failure → auto-fallback
- Low VRAM detection → 4-bit quantization
- No GPU → CPU offload with warning

✅ **Generation Error Recovery**
- OOM errors → partial video recovery
- Runtime errors → retry option
- Timeouts → graceful cancellation
- Invalid input → validation errors

✅ **Queue & Async Resilience**
- Crashing jobs → automatic removal
- Max queue size → clear rejection messages
- Concurrent submissions → proper ordering

✅ **File & Storage Safety**
- Disk full → cleanup + error
- Auto-cleanup of old files
- Safe temp path generation (no collisions)

✅ **Input Validation**
- Duration limits enforced
- XSS prevention
- Scene count limits

## 📊 Test Results

```bash
$ pytest test_app.py -v --cov=app --cov=utils

========================= test session starts =========================
test_app.py::TestModelLoadingFallback::test_primary_model_load_fails_falls_to_cogvideox_5b PASSED
test_app.py::TestModelLoadingFallback::test_low_vram_forces_4bit_quantization PASSED
test_app.py::TestGenerationErrorRecovery::test_oom_error_returns_partial_video PASSED
test_app.py::TestQueueResilience::test_max_queue_size_rejects_new_jobs PASSED
...
========================= 45 passed in 2.34s =========================

---------- coverage: platform linux, python 3.10 -----------
Name      Stmts   Miss  Cover
-----------------------------
app.py      180     15    92%
utils.py    320     18    94%
-----------------------------
TOTAL       500     33    93%
```

## 🐳 Docker Usage

### Build

```bash
# Production build
docker build -t text-to-video-app:latest .

# Test build (runs tests)
docker build --target test -t text-to-video-app:test .
```

### Run

```bash
# Basic run
docker run -p 7860:7860 text-to-video-app:latest

# With GPU support
docker run --gpus all -p 7860:7860 text-to-video-app:latest

# With custom output directory
docker run -p 7860:7860 -v $(pwd)/outputs:/app/outputs text-to-video-app:latest

# With environment variables
docker run -p 7860:7860 -e DEBUG_MODE=true -e PORT=8080 text-to-video-app:latest
```

## 🔄 CI/CD

### GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

1. Runs tests on Python 3.10, 3.11
2. Generates coverage reports
3. Uploads coverage to Codecov (optional)
4. Builds Docker image
5. Runs Docker tests

See `.github/workflows/ci.yml` for full configuration.

### Local CI Simulation

```bash
# Run the same tests as CI
pytest test_app.py -v --cov=app --cov=utils --cov-report=xml

# Build Docker image
docker build -t text-to-video-app .

# Run in container
docker run --rm text-to-video-app python -m pytest test_app.py
```

## 🐛 Debugging

### Enable Debug Mode

```bash
export DEBUG_MODE=true
python app.py
```

### View Logs

```bash
# Application logs
tail -f app.log

# Docker logs
docker logs -f <container_id>
```

### Common Issues

**Out of Memory Errors**
- Reduce resolution (512x512 instead of 1024x1024)
- Reduce duration
- Use smaller models (2B instead of 5B)

**Model Loading Fails**
- Check GPU availability: `nvidia-smi`
- Verify CUDA installation: `python -c "import torch; print(torch.cuda.is_available())"`
- Try CPU fallback mode

**Queue Full**
- Wait for current jobs to complete
- Increase `MAX_QUEUE_SIZE` in environment
- Check system resources

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `pytest test_app.py -v`
5. Submit a pull request

## 🙏 Acknowledgments

- Open-Sora project
- CogVideoX team
- Stable Video Diffusion (Stability AI)
- Gradio team

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with ❤️ using open-source models only**
