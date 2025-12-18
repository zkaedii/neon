# 🚀 Neon Tokyo Workspace Configuration

Complete workspace setup guide for the Neon Tokyo project.

## 📋 Table of Contents

1. [Quick Setup](#quick-setup)
2. [Development Environment](#development-environment)
3. [Production Deployment](#production-deployment)
4. [Configuration Files](#configuration-files)
5. [Best Practices](#best-practices)

## 🎯 Quick Setup

### One-Command Setup

```bash
# Clone and setup
git clone https://github.com/zkaedii/neon-tokyo.git
cd neon-tokyo
npm install
cd text-to-video-app && pip install -r requirements.txt && cd ..
npm run prepare  # Setup Git hooks
```

### Verify Installation

```bash
# Check Node.js
node --version  # Should be >= 18.0.0

# Check Python
python --version  # Should be >= 3.10

# Check Docker
docker --version
docker-compose --version

# Run tests
npm run test
```

## 🛠️ Development Environment

### VS Code Setup

Recommended extensions:
- ESLint
- Prettier
- Python
- Docker
- GitLens

Settings (`.vscode/settings.json`):
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "[html]": {
    "editor.formatOnSave": true
  },
  "[javascript]": {
    "editor.formatOnSave": true
  }
}
```

### Environment Variables

Create `.env` file:
```env
# Development
DEBUG_MODE=true
PORT=7860
OUTPUT_DIR=./outputs
TEMP_DIR=./temp

# Production (override in production)
GRAFANA_PASSWORD=change-me-in-production
```

### Hot Reload Development

```bash
# Terminal 1: LED Visualizer
npm run dev:led

# Terminal 2: Video Service
npm run dev:video

# Or both together
npm run dev
```

## 🚢 Production Deployment

### Prerequisites

1. **Server Requirements**:
   - Ubuntu 20.04+ or similar
   - Docker & Docker Compose installed
   - GPU support (for video generation)
   - Minimum 16GB RAM
   - 100GB+ disk space

2. **SSH Access**:
   ```bash
   ssh-keygen -t ed25519 -C "deploy@neon-tokyo"
   # Add public key to server
   ```

3. **GitHub Secrets** (for CI/CD):
   - `PRODUCTION_HOST`: Server IP/domain
   - `PRODUCTION_USER`: SSH username
   - `PRODUCTION_SSH_KEY`: Private SSH key
   - `GRAFANA_PASSWORD`: Grafana admin password
   - `SLACK_WEBHOOK`: (Optional) Slack notifications

### Deployment Steps

1. **Initial Server Setup**:
   ```bash
   # On server
   mkdir -p /opt/neon-tokyo
   cd /opt/neon-tokyo
   git clone https://github.com/zkaedii/neon-tokyo.git .
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   nano .env  # Edit with production values
   ```

3. **Deploy**:
   ```bash
   # Manual
   docker-compose -f docker-compose.prod.yml up -d

   # Or via CI/CD (automatic on push to main)
   git push origin main
   ```

4. **Verify**:
   ```bash
   # Check services
   docker-compose -f docker-compose.prod.yml ps

   # Check logs
   docker-compose -f docker-compose.prod.yml logs -f

   # Health checks
   curl http://localhost:8080/health
   curl http://localhost:7860
   ```

## 📁 Configuration Files

### Key Configuration Files

| File | Purpose |
|------|---------|
| `package.json` | Node.js workspace configuration |
| `.prettierrc.json` | Code formatting rules |
| `.eslintrc.json` | JavaScript linting rules |
| `docker-compose.prod.yml` | Production orchestration |
| `nginx.conf` | Web server configuration |
| `monitoring/prometheus.yml` | Metrics collection |
| `.github/workflows/*.yml` | CI/CD pipelines |

### Customization

#### Scene Presets
Edit `scene-preset-schema.json`:
- Color palettes
- Animation parameters
- Audio mappings
- Lighting effects

#### Video Generation
Edit `text-to-video-app/app.py`:
- Model selection
- Generation parameters
- Queue settings

#### Monitoring
Edit `monitoring/grafana/dashboards/`:
- Custom dashboards
- Alert rules
- Metrics visualization

## ✅ Best Practices

### Code Quality

1. **Before Committing**:
   ```bash
   npm run format
   npm run lint
   npm run test
   ```

2. **Commit Messages**:
   ```
   feat(led): Add new neon effect
   fix(video): Resolve memory leak
   docs: Update README
   ```

3. **Pull Requests**:
   - All tests must pass
   - Code must be formatted
   - Coverage must not decrease
   - Documentation updated

### Security

1. **Never commit**:
   - `.env` files
   - API keys
   - Private keys
   - Passwords

2. **Always**:
   - Use environment variables
   - Validate user input
   - Sanitize outputs
   - Keep dependencies updated

### Performance

1. **Optimization Checklist**:
   - [ ] Images optimized
   - [ ] Code minified (production)
   - [ ] Caching enabled
   - [ ] Database queries optimized
   - [ ] GPU utilization monitored

2. **Monitoring**:
   - Check Grafana dashboards regularly
   - Set up alerts for errors
   - Monitor resource usage
   - Review logs weekly

## 🔍 Troubleshooting

### Common Issues

**Issue**: Docker build fails
```bash
# Solution: Clear Docker cache
docker system prune -a
docker-compose -f docker-compose.prod.yml build --no-cache
```

**Issue**: Services won't start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check ports
netstat -tulpn | grep -E '8080|7860|3000'
```

**Issue**: GPU not detected
```bash
# Check NVIDIA Docker runtime
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# Verify docker-compose GPU config
```

**Issue**: Tests failing
```bash
# Run with verbose output
cd text-to-video-app
pytest test_app.py -v -s

# Check Python environment
python -m pip list
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [GitHub Actions](https://docs.github.com/en/actions)

## 🆘 Support

For issues or questions:
1. Check [GitHub Issues](https://github.com/zkaedii/neon-tokyo/issues)
2. Review logs: `docker-compose logs`
3. Check monitoring dashboards
4. Open a new issue with details

---

**Happy Coding! 🚀**
