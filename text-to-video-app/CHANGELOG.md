# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release
- Gradio web interface
- Model fallback chain (Open-Sora → CogVideoX-5B → CogVideoX-2B → SVD)
- Music integration
- Queue management system
- Comprehensive error handling
- Full test suite (90%+ coverage)
- Docker support
- CI/CD pipeline
- Pre-commit hooks
- Documentation

## [1.0.0] - 2024-01-XX

### Added
- Text-to-video generation from prompts
- Multiple model support with automatic fallback
- Background music integration
- Job queue with status tracking
- Input validation and sanitization
- Auto-cleanup of old files
- Health checks
- Debug mode
- Comprehensive logging

### Security
- Input sanitization (XSS prevention)
- Path traversal protection
- Resource limits enforcement

### Testing
- 45+ unit and integration tests
- Error path coverage
- Mock-based testing
- Coverage reporting

[Unreleased]: https://github.com/yourusername/text-to-video-app/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/text-to-video-app/releases/tag/v1.0.0
