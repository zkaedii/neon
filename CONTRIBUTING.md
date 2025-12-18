# Contributing to Neon Tokyo

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/zkaedii/neon-tokyo.git
   cd neon-tokyo
   ```

3. **Set up development environment**:
   ```bash
   npm install
   cd text-to-video-app && pip install -r requirements.txt && cd ..
   npm run prepare
   ```

4. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Development Workflow

### Code Style

- **JavaScript/HTML**: Follow ESLint and Prettier rules
- **Python**: Follow PEP 8 with 120 character line length
- **Commits**: Use conventional commit format (see below)

### Before Committing

```bash
# Format code
npm run format

# Lint code
npm run lint

# Run tests
npm run test
```

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

**Examples**:
```
feat(led): Add new neon pulse effect
fix(video): Resolve memory leak in queue
docs: Update README with deployment instructions
```

## 🧪 Testing

### Running Tests

```bash
# All tests
npm run test

# Python tests with coverage
cd text-to-video-app
make test-cov
```

### Writing Tests

- Write tests for all new features
- Maintain >90% code coverage
- Test error paths
- Test edge cases

## 📋 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Create Pull Request** with clear description

### PR Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No console.log statements (use proper logging)
- [ ] No hardcoded values
- [ ] Error handling implemented

## 🐛 Reporting Bugs

Use the GitHub issue template and include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Node version, Python version)
- Screenshots if applicable

## 💡 Suggesting Features

Use the GitHub feature request template and include:
- Clear description
- Use case
- Proposed solution
- Alternatives considered

## 📚 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect different viewpoints

## 🎯 Areas for Contribution

- New LED scene effects
- Performance optimizations
- Documentation improvements
- Test coverage
- Bug fixes
- UI/UX enhancements

## ❓ Questions?

- Open a GitHub Discussion
- Check existing issues
- Review documentation

Thank you for contributing! 🚀
