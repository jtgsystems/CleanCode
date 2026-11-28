# Contributing to ENHANCER

Thank you for considering contributing to ENHANCER! This document provides guidelines and instructions for contributing.

## Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd CleanCode
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Quality Standards

### Linting

We use `ruff` for linting and code formatting:

```bash
# Check for issues
ruff check .

# Auto-fix issues
ruff check . --fix

# Format code
ruff format .
```

All code must pass ruff checks before being merged.

### Type Checking

We use `mypy` for static type checking:

```bash
mypy ENHANCER/
```

While we don't require 100% type coverage, new code should include type hints where practical.

### Testing

We use `pytest` for testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ENHANCER --cov-report=term-missing

# Run specific test file
pytest tests/test_config.py

# Run with verbose output
pytest -v
```

**Requirements**:
- All new features must include tests
- Bug fixes should include regression tests
- Aim for >80% code coverage
- All tests must pass before merging

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable and function names
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes
- Include type hints for function parameters and return values

Example:

```python
def analyze_file(
    file_path: Path,
    auto_analyze: bool = True
) -> Optional[AnalysisResult]:
    """
    Analyze a Python file.

    Args:
        file_path: Path to the Python file
        auto_analyze: Whether to perform automatic analysis

    Returns:
        AnalysisResult object or None if analysis fails
    """
    # Implementation here
    pass
```

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense (Add, Fix, Update, Remove)
- Keep the first line under 72 characters
- Add detailed description in the body if needed

Good examples:
```
Add support for Python 3.12
Fix memory leak in file analyzer
Update dependencies to latest versions
Remove deprecated configuration options
```

## Pull Request Process

1. Fork the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the code quality standards

3. Add or update tests as needed

4. Run the full test suite and linters:
   ```bash
   ruff check .
   mypy ENHANCER/
   pytest
   ```

5. Commit your changes with clear commit messages

6. Push to your fork and create a pull request

7. Ensure CI checks pass

8. Wait for review and address feedback

## Adding New Features

When adding new features:

1. **Discuss first**: Open an issue to discuss major changes before implementing
2. **Update docs**: Update README.md and relevant documentation
3. **Add tests**: Include comprehensive tests for the new feature
4. **Update CHANGELOG**: Add an entry to CHANGELOG.md (if it exists)
5. **Type hints**: Include type hints in new code
6. **Security**: Consider security implications and update SECURITY.md if needed

## Bug Reports

When reporting bugs, include:

- **Description**: Clear description of the bug
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: Python version, OS, relevant package versions
- **Code samples**: Minimal code to reproduce the issue

## Feature Requests

For feature requests, include:

- **Use case**: Describe the problem you're trying to solve
- **Proposed solution**: Your ideas for how to implement it
- **Alternatives**: Other solutions you've considered
- **Impact**: Who would benefit from this feature

## Questions and Support

- Check existing issues and documentation first
- Open a new issue with the "question" label
- Be patient and respectful

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- The project's README.md (for significant contributions)
- Git commit history
- Release notes

Thank you for contributing to ENHANCER!
