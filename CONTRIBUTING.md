# Contributing to Turkish Legal AI Assistant

Welcome to the Turkish Legal AI Assistant project! This guide will help you understand our development process and standards.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Documentation Guidelines](#documentation-guidelines)
- [Git Workflow](#git-workflow)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Getting Started

1. **Fork and Clone**

   ```bash
   git clone https://github.com/YOUR-USERNAME/legal-ai.git
   cd legal-ai
   git remote add upstream https://github.com/ORIGINAL-OWNER/legal-ai.git
   ```

2. **Set Up Development Environment**

   ```bash
   # Install dependencies
   pip install -r requirements.txt

   # Install development tools
   pip install pre-commit
   pre-commit install

   # Install GitHub CLI for PR automation
   brew install gh  # For macOS
   gh auth login
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/123-feature-name
   ```

## Development Workflow

### Project Structure

```
backend/
├── app/          # Main application code
├── src/          # Core business logic
├── tests/        # Test files
└── README.md     # Component documentation

docs/             # Technical documentation
tools/            # Development and automation tools
```

### Automated Workflow Tool

We provide a git workflow automation tool to streamline the development process:

```bash
./.github/scripts/git_workflow.py --type TYPE --description "Your commit message"
```

This tool:

- Runs pre-commit checks
- Stages changes
- Creates conventional commits
- Pushes to remote
- Creates pull requests

For detailed usage, see [.github/scripts/git_workflow.md](.github/scripts/git_workflow.md).

## Code Standards

### Python Guidelines

- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters (Black formatter)
- Docstrings for all public functions and classes

### Pre-commit Hooks

All code must pass the following checks:

- Black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)
- prettier (markdown/yaml formatting)

## Documentation Guidelines

### Required Documentation

1. **Code Documentation**

   - Docstrings for all public APIs
   - Inline comments for complex logic
   - Type hints for all functions

2. **Component Documentation**

   - README.md in each major component
   - API documentation for endpoints
   - Usage examples

3. **Change Documentation**
   - Update CHANGELOG.md
   - Update README.md if needed
   - Document breaking changes

## Git Workflow

### Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch
- Feature branches: `feature/123-feature-name`
- Bug fixes: `fix/123-bug-name`
- Hotfixes: `hotfix/123-issue-name`

### Commit Standards

Format: `<type>(<scope>): <description>`

Types:

- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing changes
- `chore`: Maintenance tasks

Example:

```
feat(rag): implement new prompt template system

- Added template validation
- Improved error handling
- Updated documentation

Fixes #123
```

## Pull Request Process

1. **Before Submitting**

   - Update documentation
   - Add/update tests
   - Run pre-commit hooks
   - Update CHANGELOG.md

2. **PR Requirements**

   - Fill out PR template
   - Link related issues
   - Include test results
   - Add screenshots for UI changes

3. **Review Process**
   - Two approvals required
   - All CI checks must pass
   - No merge conflicts
   - All discussions resolved

## Release Process

1. **Prepare Release**

   - Create release branch (`release/vX.Y.Z`)
   - Update version numbers
   - Update CHANGELOG.md
   - Run full test suite

2. **Release Checklist**

   - Documentation updated
   - Tests passing
   - CHANGELOG.md updated
   - Version bumped
   - Release notes prepared

3. **Post-Release**
   - Tag release
   - Merge to main
   - Clean up branches
   - Update develop

## Questions and Support

- Open an issue with the "question" label
- Tag relevant maintainers
- Check existing documentation first
- Join our community discussions

## License

By contributing, you agree that your contributions will be licensed under the project's license.
