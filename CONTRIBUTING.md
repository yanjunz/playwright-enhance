# Contributing to Playwright Enhance

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/playwright-enhance/playwright-enhance.git
   cd playwright-enhance
   ```

2. **Install dependencies**
   ```bash
   pip install -e ".[dev]"
   playwright install chromium
   ```

3. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and write tests**
   - Add unit tests in `tests/unit/`
   - Add integration tests in `tests/integration/`
   - Ensure >90% code coverage

3. **Run linters and tests**
   ```bash
   black .
   ruff check . --fix
   mypy playwright_enhance
   pytest
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for formatting (100 char line length)
- Use type hints for all function signatures
- Write docstrings for public APIs

## Testing Guidelines

- Write tests for all new features
- Maintain >90% code coverage
- Use descriptive test names: `test_<feature>_<scenario>_<expected_result>`
- Mock external dependencies (Playwright, OpenCV)

## Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `chore:` - Build/tooling changes

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure CI passes
4. Request review from maintainers
5. Address review feedback

## Questions?

Open an issue or discussion on GitHub.
