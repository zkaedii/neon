# Workspace Rules and Standards

This document defines the rules, standards, and best practices for working in this codebase.

## 📋 Table of Contents

1. [Code Standards](#code-standards)
2. [File Organization](#file-organization)
3. [Naming Conventions](#naming-conventions)
4. [Error Handling Rules](#error-handling-rules)
5. [Testing Requirements](#testing-requirements)
6. [Documentation Standards](#documentation-standards)
7. [Git Workflow](#git-workflow)
8. [Performance Guidelines](#performance-guidelines)
9. [Security Rules](#security-rules)

## Code Standards

### Python Version

- **Minimum**: Python 3.10
- **Recommended**: Python 3.11
- Use type hints for all function signatures
- Follow PEP 8 with 120 character line length

### Code Formatting

**Required Tools:**
- Black (line length: 120)
- isort (profile: black)

**Before Committing:**
```bash
make format
```

### Linting Rules

**Tools:**
- flake8 (max line length: 120)
- mypy (type checking)
- bandit (security)

**Rules:**
- Maximum complexity: 15
- No unused imports
- No unused variables
- All public functions must have docstrings

### Import Organization

```python
# Standard library
import os
import sys
from pathlib import Path
from typing import Optional, Dict

# Third-party
import torch
import gradio as gr

# Local
from utils import ErrorHandler, ModelLoader
```

## File Organization

### Directory Structure

```
text-to-video-app/
├── app.py              # Main application entry point
├── utils.py            # Utility functions and classes
├── test_app.py         # Test suite
├── requirements.txt    # Production dependencies
├── setup.cfg           # Package configuration
├── pyproject.toml      # Build and tool configuration
├── Dockerfile          # Container definition
├── Makefile           # Common commands
├── README.md          # Main documentation
├── CONTRIBUTING.md    # Contribution guidelines
├── WORKSPACE_RULES.md # This file
├── .editorconfig     # Editor configuration
├── .pre-commit-config.yaml  # Pre-commit hooks
├── .vscode/           # VS Code settings
└── .github/           # GitHub workflows and templates
```

### File Naming

- **Python files**: `snake_case.py`
- **Test files**: `test_*.py` or `*_test.py`
- **Config files**: `.filename` or `filename.ext`
- **Documentation**: `UPPERCASE.md`

## Naming Conventions

### Variables and Functions

```python
# Good
def generate_video(prompt: str) -> str:
    video_path = create_output_path()
    return video_path

# Bad
def genVid(p: str):
    vp = createPath()
    return vp
```

### Classes

```python
# Good
class ModelLoader:
    def load_model(self):
        pass

# Bad
class model_loader:
    def LoadModel(self):
        pass
```

### Constants

```python
# Good
MAX_QUEUE_SIZE = 50
OUTPUT_DIR = Path("./outputs")

# Bad
maxQueueSize = 50
output_dir = Path("./outputs")
```

## Error Handling Rules

### Always Use Try-Except

```python
# Good
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    return fallback_value

# Bad
result = risky_operation()  # May crash
```

### Error Types

1. **User Errors**: Validation errors, input errors
   - Return user-friendly messages
   - Log technical details

2. **System Errors**: OOM, timeouts, I/O errors
   - Log with full context
   - Provide recovery options when possible

3. **Unexpected Errors**: Unknown exceptions
   - Log with traceback
   - Return generic user message
   - Include technical details in debug mode

### Error Logging

```python
# Always include context
error_handler.log_error(
    error=exception,
    context="model_loading",
    include_traceback=True
)
```

## Testing Requirements

### Coverage Requirements

- **Overall**: ≥90%
- **Error Handling**: ≥95%
- **Critical Functions**: 100%

### Test Structure

```python
class TestFeatureName:
    """Test suite for FeatureName."""
    
    def test_normal_case(self):
        """Test normal operation."""
        ...
    
    def test_error_case(self):
        """Test error handling."""
        ...
```

### Test Naming

- Format: `test_<what>_<condition>_<expected>`
- Example: `test_model_loading_fails_falls_to_fallback`

### Required Test Categories

1. **Unit Tests**: Individual functions
2. **Integration Tests**: Component interactions
3. **Error Path Tests**: All failure scenarios
4. **Edge Case Tests**: Boundary conditions

## Documentation Standards

### Docstring Format

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description (one line).
    
    Longer description if needed (multiple lines).
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param1 is invalid
        RuntimeError: When operation fails
    
    Example:
        >>> function_name("test", 42)
        True
    """
    ...
```

### Code Comments

- Explain **why**, not **what**
- Use comments for complex logic
- Keep comments up-to-date

```python
# Good: Explains why
# Use 4-bit quantization to reduce VRAM usage below 8GB threshold
model = load_quantized_model()

# Bad: Explains what (obvious from code)
# Load the model
model = load_model()
```

## Git Workflow

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `test/description` - Test additions
- `refactor/description` - Code refactoring

### Commit Messages

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Refactoring
- `style`: Formatting
- `chore`: Maintenance

### Commit Frequency

- Commit often, push when feature complete
- Each commit should be a logical unit
- Use `--fixup` for addressing review comments

## Performance Guidelines

### Optimization Rules

1. **Profile First**: Don't optimize prematurely
2. **Measure**: Use profiling tools
3. **Optimize Hot Paths**: Focus on bottlenecks
4. **Document**: Explain performance decisions

### Resource Management

```python
# Good: Explicit resource management
with open(file_path) as f:
    data = f.read()

# Good: Cleanup in finally
try:
    result = operation()
finally:
    cleanup_resources()
```

### Memory Management

- Clean up large objects promptly
- Use generators for large datasets
- Monitor GPU memory usage
- Implement auto-cleanup for temp files

## Security Rules

### Input Validation

- **Always validate** user inputs
- **Sanitize** text inputs (prevent XSS)
- **Limit** resource usage (duration, resolution)
- **Check** file paths (prevent path traversal)

### Secrets Management

- **Never commit** API keys or secrets
- **Use environment variables** for configuration
- **Use .env files** for local development (gitignored)
- **Rotate** credentials regularly

### Dependency Security

```bash
# Check for vulnerabilities
bandit -r app.py utils.py
pip-audit
```

## Code Review Checklist

Before submitting PR:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Coverage maintained/improved
- [ ] Documentation updated
- [ ] No security issues (bandit clean)
- [ ] Error handling comprehensive
- [ ] Performance acceptable
- [ ] No hardcoded values
- [ ] Environment variables used appropriately

## Enforcement

### Automated Checks

- **Pre-commit hooks**: Format, lint, type-check
- **CI/CD**: Full test suite, coverage check
- **GitHub Actions**: Automated PR checks

### Manual Review

- All PRs require review
- Maintainers enforce standards
- Feedback provided constructively

## Exceptions

If you need to deviate from these rules:

1. **Document why** in code comments
2. **Get approval** from maintainers
3. **Update rules** if pattern becomes common

## Questions?

- Check existing code for examples
- Ask in PR comments
- Open a discussion issue
- Review CONTRIBUTING.md

---

**Remember**: These rules exist to maintain code quality and make collaboration easier. When in doubt, ask!
