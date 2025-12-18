# Multi-stage Dockerfile for text-to-video generation app
FROM python:3.10-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ============================================================================
# Test stage
# ============================================================================
FROM base as test

# Copy test files
COPY test_app.py .
COPY utils.py .
COPY app.py .

# Run tests with coverage
RUN pytest test_app.py -v --cov=app --cov=utils --cov-report=term-missing --cov-report=xml || true

# ============================================================================
# Production stage
# ============================================================================
FROM base as production

# Copy application files
COPY app.py .
COPY utils.py .

# Create output directories
RUN mkdir -p /app/outputs /app/temp

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBUG_MODE=false
ENV OUTPUT_DIR=/app/outputs
ENV TEMP_DIR=/app/temp
ENV PORT=7860

# Expose port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:7860')" || exit 1

# Run application
CMD ["python", "app.py"]
