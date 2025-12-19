# 🌃 Neon Tokyo - Advanced Cyberpunk LED Scene Visualizer & Text-to-Video Platform

<div align="center">

![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge&logo=github&logoColor=white)
![Version](https://img.shields.io/badge/version-2.0.0-blue?style=for-the-badge&logo=tag&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge&logo=open-source-initiative&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-18%2B-339933?style=for-the-badge&logo=node.js&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Cyberpunk](https://img.shields.io/badge/cyberpunk-neon--tokyo-00f5ff?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMTMuMDkgOC4yNkwyMCA5TDEzLjA5IDE1Ljc0TDEyIDIyTDEwLjkxIDE1Ljc0TDQgOUwxMC45MSA4LjI2TDEyIDJaIiBmaWxsPSIjMDBmNWZmIi8+Cjwvc3ZnPgo=&logoColor=white)
![AI Powered](https://img.shields.io/badge/AI-Powered-FF6B9D?style=for-the-badge&logo=brain&logoColor=white)
![WebGL](https://img.shields.io/badge/WebGL-Accelerated-990000?style=for-the-badge&logo=webgl&logoColor=white)
![FPS](https://img.shields.io/badge/FPS-60-brightgreen?style=for-the-badge&logo=gamepad&logoColor=white)

[![GitHub Stars](https://img.shields.io/github/stars/zkaedii/neon?style=for-the-badge&logo=github&logoColor=white&labelColor=181717&color=gold)](https://github.com/zkaedii/neon)
[![GitHub Forks](https://img.shields.io/github/forks/zkaedii/neon?style=for-the-badge&logo=github&logoColor=white&labelColor=181717&color=blue)](https://github.com/zkaedii/neon)
[![GitHub Issues](https://img.shields.io/github/issues/zkaedii/neon?style=for-the-badge&logo=github&logoColor=white&labelColor=181717&color=orange)](https://github.com/zkaedii/neon/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/zkaedii/neon?style=for-the-badge&logo=github&logoColor=white&labelColor=181717&color=purple)](https://github.com/zkaedii/neon/pulls)

![Code Quality](https://img.shields.io/badge/code--quality-A%2B-success?style=for-the-badge&logo=code-review&logoColor=white)
![Maintained](https://img.shields.io/badge/maintained-yes-success?style=for-the-badge&logo=check-circle&logoColor=white)
![Production Ready](https://img.shields.io/badge/production-ready-true-success?style=for-the-badge&logo=rocket&logoColor=white)
![Zero Downtime](https://img.shields.io/badge/zero--downtime-deploy-success?style=for-the-badge&logo=cloudflare&logoColor=white)
![ESLint](https://img.shields.io/badge/ESLint-enabled-4B32C3?style=for-the-badge&logo=eslint&logoColor=white)
![Prettier](https://img.shields.io/badge/Prettier-formatted-F7B93E?style=for-the-badge&logo=prettier&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-ready-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-UI-FF6B6B?style=for-the-badge&logo=gradio&logoColor=white)
![Open Sora](https://img.shields.io/badge/Open--Sora-integrated-00D9FF?style=for-the-badge&logo=openai&logoColor=white)
![Stable Video](https://img.shields.io/badge/Stable--Video-Diffusion-FF6B35?style=for-the-badge&logo=stability-ai&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-monitoring-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-dashboards-F46800?style=for-the-badge&logo=grafana&logoColor=white)

</div>

<div align="center">
  <strong>A mind-blowing, production-ready platform fusing real-time LED scene visualization with AI-powered text-to-video generation.</strong><br>
  Immerse in neon-drenched futures—where computational physics meets creative emergence.
</div>

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
neon-tokyo/
├── remixed-badc0925.html # LED Scene Visualizer (Frontend)
├── scene-preset-schema.json # Scene configuration schema
├── text-to-video-app/ # Video generation service (Python/Gradio)
├── monitoring/ # Prometheus & Grafana configs
├── scripts/ # Deployment scripts
└── docker-compose.prod.yml # Production orchestration
text## 🚀 Quick Start

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
Access:

LED Visualizer: http://localhost:8080
Text-to-Video: http://localhost:7860

Production Deployment
Bash# Using Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Or use deployment script
chmod +x scripts/deploy-production.sh
./scripts/deploy-production.sh
📋 Available Commands
Development
Bashnpm run dev             # Start all development servers
npm run dev:led         # Start LED visualizer only
npm run dev:video       # Start video generation service
npm run build           # Build all components
npm run lint            # Lint all code
npm run format          # Format all code
npm run test            # Run test suite
npm run test:coverage   # Run tests with coverage
Docker
Bashnpm run docker:build    # Build Docker images
npm run docker:up       # Start containers
npm run docker:down     # Stop containers
npm run docker:logs     # View container logs
Deployment
Bashnpm run deploy:staging  # Deploy to staging
npm run deploy:production # Deploy to production
🔧 Configuration
Environment Variables
Create .env in project root:
env# Application
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
Scene Presets
Edit scene-preset-schema.json:
JSON{
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
🧪 Testing
Bashnpm run test                    # Run all tests

# Python tests with coverage
cd text-to-video-app
make test-cov
open htmlcov/index.html         # View coverage report
📊 Monitoring

Grafana: http://localhost:3000 (admin/admin)
Prometheus: http://localhost:9090

Pre-configured dashboards: System metrics • Video generation performance • Queue status • Error rates
🔒 Security

Input validation and sanitization
XSS prevention
Security headers (CORS, CSP)
Automated security scanning (Trivy, Bandit)
Secrets management via environment variables

🛠️ Development Tools
Code Quality

ESLint: JavaScript/HTML linting
Prettier: Code formatting
Black: Python formatting
isort: Import sorting
mypy: Type checking
Bandit: Security scanning

Git Hooks

Pre-commit: Format & lint
Pre-push: Run tests
Commit-msg: Validate messages

📦 Project Structure
textneon-tokyo/
├── .github/
│   └── workflows/              # CI/CD pipelines
├── monitoring/                 # Prometheus & Grafana
├── scripts/                    # Deployment scripts
├── text-to-video-app/          # Video generation service
│   ├── app.py                  # Main application
│   ├── utils.py                # Utilities
│   ├── test_app.py             # Tests
│   └── requirements.txt        # Dependencies
├── docker-compose.prod.yml     # Production orchestration
├── nginx.conf                  # Nginx configuration
├── package.json                # Node.js workspace config
└── README.md                   # This file
🚢 Deployment
CI/CD Pipeline
Automated on push to main:

Run tests
Lint code
Build Docker images
Deploy to production
Health checks
Notifications

Manual Deployment
Bash# Staging
./scripts/deploy-staging.sh

# Production
./scripts/deploy-production.sh
🤝 Contributing

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Make changes and test
Commit (git commit -m 'feat: Add amazing feature')
Push (git push origin feature/amazing-feature)
Open a Pull Request

See CONTRIBUTING.md for details.
📝 License
MIT License - see LICENSE file.
🙏 Acknowledgments

Open-Sora project
CogVideoX team
Stable Video Diffusion (Stability AI)
Gradio team
All contributors

📧 Support

Issues: GitHub Issues
Discussions: GitHub Discussions



  Built with ❤️ and lots of ☕ by the Neon Tokyo team

  Experience the future of creative technology 🚀

```
