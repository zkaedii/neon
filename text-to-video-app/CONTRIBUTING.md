# Contributing Guidelines

Thank you for your interest in contributing to the Text-to-Video Generator! This document provides guidelines and standards for contributions.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Maintain professional communication

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/yourusername/text-to-video-app.git
cd text-to-video-app
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies
make install-dev
# or
pip install -e ".[dev]"
```

### 4. Install Pre-commit Hooks

```bash
pre-commit install
```

## Coding Standards

### Python Style Guide

- Follow PEP 8 with line length of 120 characters
- Use type hints where possible
- Write docstrings for all public functions/classes
- Keep functions focused and small (< 50 lines when possible)
- Maximum complexity: 15 (as measured by flake8)

### Code Formatting

We use automated formatting tools:

```bash
# Format code
make format

# Check formatting
make format-check
```

**Tools:**
- **Black**: Code formatter (line length: 120)
- **isort**: Import sorter (profile: black)

### Linting

```bash
# Run linters
make lint
```

**Tools:**
- **flake8**: Style guide enforcement
- **mypy**: Static type checking
- **bandit**: Security linting

### Type Hints

- Use type hints for function parameters and return values
- Use `Optional[T]` for nullable types
- Use `Dict[str, Any]` for flexible dictionaries
- Import types from `typing` module

Example:
```python
from typing import Optional, Dict, Any, List

def process_data(
    input_data: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None
) -> List[str]:
    """Process input data and return results."""
    ...
```

## Testing Requirements

### Test Coverage

- **Minimum coverage**: 90%
- **Error handling paths**: 95%+
- **Critical functions**: 100%

### Writing Tests

1. **Test Structure**
   - Use pytest fixtures for setup/teardown
   - Group related tests in classes
   - Use descriptive test names: `test_<what>_<condition>_<expected_result>`

2. **Test Categories**
   - **Unit tests**: Test individual functions in isolation
   - **Integration tests**: Test component interactions
   - **Error path tests**: Test all failure scenarios

3. **Test Example**

```python
def test_model_loading_fallback_on_failure(model_loader):
    """Test model fallback when primary model fails."""
    with patch.object(model_loader, '_load_open_sora', side_effect=RuntimeError):
        model, name = model_loader.load_with_fallback()
        assert name == "cogvideox-5b"
```

### Running Tests

```bash
# All tests with coverage
make test

# Fast tests (no coverage)
make test-fast

# Specific test
make test-specific TEST=TestModelLoadingFallback::test_primary_model_load_fails
```

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `style`: Code style changes (formatting)
- `chore`: Maintenance tasks

**Examples:**
```
feat(model): add CogVideoX-2B fallback support

- Implement model loading for CogVideoX-2B
- Add CPU fallback capability
- Update tests for new fallback path

Closes #123
```

### Pre-commit Checks

Before committing, ensure:

```bash
# Run all checks
make check-all

# Or individually
make format-check
make lint
make type-check
make test-fast
```

## Pull Request Process

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code following standards
- Add tests for new functionality
- Update documentation if needed
- Ensure all tests pass

### 3. Commit Changes

```bash
git add .
git commit -m "feat(scope): your commit message"
```

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

### PR Requirements

- [ ] All tests pass (`make test`)
- [ ] Code is formatted (`make format-check`)
- [ ] Linters pass (`make lint`)
- [ ] Type checking passes (`make type-check`)
- [ ] Coverage maintained or improved
- [ ] Documentation updated if needed
- [ ] Commit messages follow guidelines

### PR Review Process

1. Automated CI checks must pass
2. At least one maintainer review required
3. Address review comments
4. Maintainer will merge when approved

## Error Handling Guidelines

### Always Handle Errors

```python
# Good
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    return fallback_value

# Bad
result = risky_operation()  # May crash
```

### Error Messages

- **User-facing**: Friendly, actionable messages
- **Logging**: Technical details with context
- **Debug mode**: Full tracebacks

### Test Error Paths

Every error path must have a test:

```python
def test_handles_oom_error_gracefully():
    """Test OOM error returns partial video."""
    with patch('torch.cuda.OutOfMemoryError'):
        result = generate_video(...)
        assert result is not None
```

## Documentation

### Code Documentation

- **Docstrings**: All public functions/classes
- **Type hints**: For better IDE support
- **Comments**: Explain "why", not "what"

### Docstring Format

```python
def process_data(data: Dict[str, Any]) -> List[str]:
    """
    Process input data and return formatted results.
    
    Args:
        data: Dictionary containing input data with keys 'input' and 'options'
    
    Returns:
        List of processed string results
    
    Raises:
        ValueError: If data format is invalid
    
    Example:
        >>> process_data({"input": "test", "options": {}})
        ['processed_test']
    """
    ...
```

## Project Structure

```
text-to-video-app/
├── app.py              # Main application
├── utils.py            # Utilities and helpers
├── test_app.py         # Test suite
├── requirements.txt    # Dependencies
├── Dockerfile          # Container config
├── README.md          # Main documentation
├── CONTRIBUTING.md    # This file
└── .github/           # CI/CD configs
```

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones

Thank you for contributing! 🎉
