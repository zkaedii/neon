#!/bin/bash
set -euo pipefail

# Staging Deployment Script
# Similar to production but with relaxed checks

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting staging deployment..."

cd "$PROJECT_ROOT"

# Use development docker-compose for staging
docker-compose -f docker-compose.yml up -d --build

log "Staging deployment completed!"
log "Services available at:"
log "  - LED Visualizer: http://localhost:8080"
log "  - Text-to-Video: http://localhost:7860"
