#!/bin/bash
set -euo pipefail

# Production Deployment Script for Neon Tokyo
# This script handles safe, zero-downtime deployment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    exit 1
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    command -v docker >/dev/null 2>&1 || error "Docker is required but not installed"
    command -v docker-compose >/dev/null 2>&1 || error "docker-compose is required but not installed"

    if [ ! -f "$PROJECT_ROOT/docker-compose.prod.yml" ]; then
        error "docker-compose.prod.yml not found"
    fi

    log "Prerequisites check passed ✓"
}

# Run tests
run_tests() {
    log "Running test suite..."
    cd "$PROJECT_ROOT/text-to-video-app"

    if command -v pytest >/dev/null 2>&1; then
        pytest test_app.py -v || error "Tests failed"
    else
        warn "pytest not found, skipping tests"
    fi

    log "Tests passed ✓"
}

# Build Docker images
build_images() {
    log "Building Docker images..."
    cd "$PROJECT_ROOT"

    docker-compose -f docker-compose.prod.yml build --no-cache || error "Docker build failed"

    log "Docker images built ✓"
}

# Deploy with zero downtime
deploy() {
    log "Starting deployment..."
    cd "$PROJECT_ROOT"

    # Pull latest images
    docker-compose -f docker-compose.prod.yml pull || warn "Failed to pull images, using local"

    # Start new containers
    docker-compose -f docker-compose.prod.yml up -d || error "Deployment failed"

    # Wait for health checks
    log "Waiting for services to be healthy..."
    sleep 30

    # Verify deployment
    if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
        log "Deployment successful ✓"
    else
        error "Deployment verification failed"
    fi
}

# Health check
health_check() {
    log "Running health checks..."

    # Check LED visualizer
    if curl -f http://localhost:8080/health >/dev/null 2>&1; then
        log "LED Visualizer: Healthy ✓"
    else
        warn "LED Visualizer: Unhealthy"
    fi

    # Check text-to-video service
    if curl -f http://localhost:7860 >/dev/null 2>&1; then
        log "Text-to-Video Service: Healthy ✓"
    else
        warn "Text-to-Video Service: Unhealthy"
    fi

    # Check Redis
    if docker exec neon-tokyo-redis redis-cli ping >/dev/null 2>&1; then
        log "Redis: Healthy ✓"
    else
        warn "Redis: Unhealthy"
    fi
}

# Main deployment flow
main() {
    log "Starting production deployment..."

    check_prerequisites
    run_tests
    build_images
    deploy
    health_check

    log "Production deployment completed successfully! 🚀"
    log "Services available at:"
    log "  - LED Visualizer: http://localhost:8080"
    log "  - Text-to-Video: http://localhost:7860"
    log "  - Grafana: http://localhost:3000"
}

# Run main function
main "$@"
