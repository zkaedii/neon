# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## 🚀 Installation

```bash
# 1. Install dependencies
npm install
cd text-to-video-app && pip install -r requirements.txt && cd ..

# 2. Setup Git hooks
npm run prepare

# 3. Configure environment
cp env.example .env
# Edit .env with your settings
```

## 🎮 Start Development

```bash
# Start everything
npm run dev

# Or individually:
npm run dev:led      # LED Visualizer (http://localhost:8080)
npm run dev:video     # Video Service (http://localhost:7860)
```

## ✅ Verify Setup

```bash
# Run tests
npm run test

# Check code quality
npm run lint
npm run format
```

## 🚢 Deploy to Production

```bash
# Using Docker
docker-compose -f docker-compose.prod.yml up -d

# Or use script
./scripts/deploy-production.sh
```

## 📚 Need Help?

- **Setup Issues?** → [WORKSPACE_CONFIG.md](WORKSPACE_CONFIG.md)
- **Deployment?** → [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)
- **Contributing?** → [CONTRIBUTING.md](CONTRIBUTING.md)
- **Full Docs?** → [README.md](README.md)

---

**That's it! You're ready to build! 🎉**
