# 🚀 Production Deployment Guide

Complete guide for deploying Neon Tokyo to production.

## 📋 Prerequisites

### Server Requirements

- **OS**: Ubuntu 20.04+ or similar Linux distribution
- **RAM**: Minimum 16GB (32GB recommended)
- **Storage**: 100GB+ SSD
- **GPU**: NVIDIA GPU with CUDA support (for video generation)
- **Network**: Stable internet connection

### Software Requirements

```bash
# Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# NVIDIA Docker (for GPU support)
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

## 🔧 Initial Setup

### 1. Server Preparation

```bash
# Create application directory
sudo mkdir -p /opt/neon-tokyo
sudo chown $USER:$USER /opt/neon-tokyo
cd /opt/neon-tokyo

# Clone repository
git clone https://github.com/zkaedii/neon-tokyo.git .

# Or copy files via SCP
# scp -r ./neon-tokyo/* user@server:/opt/neon-tokyo/
```

### 2. Environment Configuration

```bash
# Copy example environment file
cp env.example .env

# Edit environment variables
nano .env
```

**Required Environment Variables**:
```env
DEBUG_MODE=false
PORT=7860
OUTPUT_DIR=/app/outputs
TEMP_DIR=/app/temp
MAX_QUEUE_SIZE=50
GRAFANA_PASSWORD=your-secure-password-here
```

### 3. SSL/TLS Setup (Recommended)

```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Generate certificates (if using Nginx)
sudo certbot --nginx -d your-domain.com
```

## 🚢 Deployment Methods

### Method 1: Docker Compose (Recommended)

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Check status
docker-compose -f docker-compose.prod.yml ps
```

### Method 2: Automated Script

```bash
# Make script executable
chmod +x scripts/deploy-production.sh

# Run deployment
./scripts/deploy-production.sh
```

### Method 3: CI/CD (GitHub Actions)

1. Configure GitHub Secrets:
   - `PRODUCTION_HOST`: Your server IP/domain
   - `PRODUCTION_USER`: SSH username
   - `PRODUCTION_SSH_KEY`: Private SSH key
   - `GRAFANA_PASSWORD`: Grafana admin password

2. Push to `main` branch:
   ```bash
   git push origin main
   ```

3. Deployment runs automatically via GitHub Actions

## ✅ Verification

### Health Checks

```bash
# LED Visualizer
curl http://localhost:8080/health

# Text-to-Video Service
curl http://localhost:7860

# Redis
docker exec neon-tokyo-redis redis-cli ping

# Prometheus
curl http://localhost:9090/-/healthy

# Grafana
curl http://localhost:3000/api/health
```

### Service Status

```bash
# Check all containers
docker-compose -f docker-compose.prod.yml ps

# Check resource usage
docker stats

# Check logs
docker-compose -f docker-compose.prod.yml logs --tail=100
```

## 🔒 Security Hardening

### Firewall Configuration

```bash
# UFW setup
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 7860/tcp  # Video service (if exposed)
sudo ufw enable
```

### Nginx Reverse Proxy (Recommended)

```nginx
# /etc/nginx/sites-available/neon-tokyo
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /video/ {
        proxy_pass http://localhost:7860/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL Configuration

```bash
# Auto-renewal setup
sudo certbot renew --dry-run

# Add to crontab
sudo crontab -e
# Add: 0 0 * * * certbot renew --quiet
```

## 📊 Monitoring

### Access Dashboards

- **Grafana**: http://your-domain.com:3000
  - Default credentials: `admin` / (from GRAFANA_PASSWORD)
- **Prometheus**: http://your-domain.com:9090

### Key Metrics to Monitor

1. **System Resources**:
   - CPU usage
   - Memory usage
   - Disk space
   - GPU utilization

2. **Application Metrics**:
   - Video generation requests
   - Queue size
   - Error rate
   - Response times

3. **Service Health**:
   - Container status
   - Health check results
   - Log errors

## 🔄 Updates & Maintenance

### Updating Application

```bash
cd /opt/neon-tokyo

# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Verify
docker-compose -f docker-compose.prod.yml ps
```

### Backup Strategy

```bash
# Backup volumes
docker run --rm -v neon-tokyo_redis-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/redis-backup-$(date +%Y%m%d).tar.gz /data

# Backup outputs
tar czf outputs-backup-$(date +%Y%m%d).tar.gz outputs/
```

### Log Management

```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Rotate logs (configure in docker-compose)
# Use logrotate or Docker logging drivers
```

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check ports
sudo netstat -tulpn | grep -E '8080|7860|3000'

# Check disk space
df -h

# Check Docker
docker ps
docker system df
```

### GPU Issues

```bash
# Verify NVIDIA Docker
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# Check GPU in container
docker exec neon-tokyo-video nvidia-smi
```

### Performance Issues

```bash
# Monitor resources
docker stats

# Check queue
docker exec neon-tokyo-video python -c "from app import job_queue; print(job_queue.qsize())"

# Review logs for errors
docker-compose -f docker-compose.prod.yml logs | grep ERROR
```

## 📞 Support

For production issues:
1. Check logs: `docker-compose logs`
2. Review monitoring dashboards
3. Check GitHub Issues
4. Contact maintainers

---

**Happy Deploying! 🚀**
