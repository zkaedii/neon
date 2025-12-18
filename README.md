# 🌃 Neon Tokyo - Advanced Cyberpunk LED Scene Visualizer & Text-to-Video Platform

[![CI Pipeline](https://github.com/zkaedii/neon-tokyo/workflows/CI%20Pipeline/badge.svg)](https://github.com/zkaedii/neon-tokyo/actions)
[![Production Deployment](https://github.com/zkaedii/neon-tokyo/workflows/Production%20Deployment/badge.svg)](https://github.com/zkaedii/neon-tokyo/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A mindblowing, production-ready platform combining real-time LED scene visualization with AI-powered text-to-video generation. Experience the future of creative technology.

## ✨ Features

### 🎨 LED Scene Visualizer
- **Real-time Cyberpunk Scenes**: Immersive neon-soaked Tokyo streets
- **Audio-Reactive**: Beat detection and frequency-based animations
- **Image Integration**: Load and display custom images in the scene
- **Scene Presets**: JSON-based configuration system for custom scenes
- **Interactive Controls**: Real-time parameter adjustment
- **Performance Optimized**: 60 FPS rendering with WebGL acceleration

### 🎬 Text-to-Video Generator
- **Multi-Model Support**: Automatic fallback chain (Open-Sora → CogVideoX → SVD)
- **Music Integration**: Add background music to generated videos
- **Queue System**: Handle concurrent requests efficiently
- **Comprehensive Error Handling**: Graceful degradation under all scenarios
- **Production-Ready**: Docker support, health checks, monitoring

### 🚀 Production Features
- **Zero-Downtime Deployments**: Automated CI/CD pipelines
- **Monitoring & Analytics**: Prometheus + Grafana dashboards
- **Security Hardened**: Security scanning, input validation
- **Scalable Architecture**: Microservices with Redis caching
- **Developer Experience**: Hot reload, comprehensive tooling

## 🏗️ Architecture

```
neon-tokyo/
├── remixed-badc0925.html      # LED Scene Visualizer (Frontend)
├── scene-preset-schema.json    # Scene configuration schema
├── text-to-video-app/          # Video generation service (Python/Gradio)
├── monitoring/                  # Prometheus & Grafana configs
├── scripts/                     # Deployment scripts
└── docker-compose.prod.yml     # Production orchestration
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Docker & Docker Compose
- CUDA-capable GPU (recommended for video generation)

### Local Development

```bash
# Clone repository
git clone https://github.com/zkaedii/neon-tokyo.git
cd neon-tokyo

# Install dependencies
npm install
cd text-to-video-app && pip install -r requirements.txt && cd ..

# Start development servers
npm run dev
```

Access:
- LED Visualizer: http://localhost:8080
- Text-to-Video: http://localhost:7860

### Production Deployment

```bash
# Using Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Or use deployment script
chmod +x scripts/deploy-production.sh
./scripts/deploy-production.sh
```

## 📋 Available Commands

### Development
```bash
npm run dev              # Start all development servers
npm run dev:led          # Start LED visualizer only
npm run dev:video        # Start video generation service
npm run build            # Build all components
npm run lint             # Lint all code
npm run format           # Format all code
npm run test             # Run test suite
npm run test:coverage    # Run tests with coverage
```

### Docker
```bash
npm run docker:build     # Build Docker images
npm run docker:up        # Start containers
npm run docker:down      # Stop containers
npm run docker:logs      # View container logs
```

### Deployment
```bash
npm run deploy:staging      # Deploy to staging
npm run deploy:production  # Deploy to production
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in project root:

```env
# Application
DEBUG_MODE=false
PORT=7860
OUTPUT_DIR=./outputs
TEMP_DIR=./temp

# Queue Settings
MAX_QUEUE_SIZE=50
MAX_FILE_AGE_DAYS=7
MAX_FILES=50

# Monitoring
GRAFANA_PASSWORD=your-secure-password

# Production
PRODUCTION_HOST=your-server.com
PRODUCTION_USER=deploy
```

### Scene Presets

Edit `scene-preset-schema.json` to customize LED scenes:

```json
{
  "metadata": {
    "name": "Your Scene",
    "bpm_range": [90, 140],
    "mood": "energetic"
  },
  "color_palette": {
    "primary": "#00f5ff",
    "secondary": "#ff00ff"
  }
}
```

## 🧪 Testing

```bash
# Run all tests
npm run test

# Python tests with coverage
cd text-to-video-app
make test-cov

# View coverage report
open htmlcov/index.html
```

## 📊 Monitoring

Access monitoring dashboards:
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

Pre-configured dashboards:
- System metrics
- Video generation performance
- Queue status
- Error rates

## 🔒 Security

- Input validation and sanitization
- XSS prevention
- Security headers (CORS, CSP)
- Automated security scanning (Trivy, Bandit)
- Secrets management via environment variables

## 🛠️ Development Tools

### Code Quality
- **ESLint**: JavaScript/HTML linting
- **Prettier**: Code formatting
- **Black**: Python formatting
- **isort**: Import sorting
- **mypy**: Type checking
- **Bandit**: Security scanning

### Git Hooks
- Pre-commit: Format & lint
- Pre-push: Run tests
- Commit-msg: Validate messages

## 📦 Project Structure

```
neon-tokyo/
├── .github/
│   └── workflows/          # CI/CD pipelines
├── monitoring/             # Prometheus & Grafana
├── scripts/                # Deployment scripts
├── text-to-video-app/      # Video generation service
│   ├── app.py              # Main application
│   ├── utils.py            # Utilities
│   ├── test_app.py         # Tests
│   └── requirements.txt    # Dependencies
├── docker-compose.prod.yml # Production orchestration
├── nginx.conf              # Nginx configuration
├── package.json            # Node.js workspace config
└── README.md               # This file
```

## 🚢 Deployment

### CI/CD Pipeline

Automated deployment on push to `main`:
1. Run tests
2. Lint code
3. Build Docker images
4. Deploy to production
5. Health checks
6. Notifications

### Manual Deployment

```bash
# Staging
./scripts/deploy-staging.sh

# Production
./scripts/deploy-production.sh
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes and test
4. Commit (`git commit -m 'feat: Add amazing feature'`)
5. Push (`git push origin feature/amazing-feature`)
6. Open a Pull Request

See [CONTRIBUTING.md](text-to-video-app/CONTRIBUTING.md) for details.

## 📝 License

MIT License - see [LICENSE](text-to-video-app/LICENSE) file for details.

## 🙏 Acknowledgments

- Open-Sora project
- CogVideoX team
- Stable Video Diffusion (Stability AI)
- Gradio team
- All contributors

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/zkaedii/neon-tokyo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/zkaedii/neon-tokyo/discussions)

---

**Built with ❤️ and lots of ☕ by the Neon Tokyo team**

*Experience the future of creative technology* 🚀
