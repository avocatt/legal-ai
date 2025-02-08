# Contributing to Turkish Legal AI Assistant

Welcome to the Turkish Legal AI Assistant project! We're excited that you're interested in contributing. This document provides guidelines and standards for contributing to our project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Documentation Guidelines](#documentation-guidelines)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. All contributors are expected to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the Repository**

   ```bash
   git clone https://github.com/YOUR-USERNAME/legal-ai.git
   cd legal-ai
   git remote add upstream https://github.com/ORIGINAL-OWNER/legal-ai.git
   ```

2. **Set Up Development Environment**

   - Install required dependencies
   - Set up pre-commit hooks

   ```bash
   pip install pre-commit
   pre-commit install
   ```

3. **Create a New Branch**
   Follow our [branch naming convention](docs/GIT_WORKFLOW.md):
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/123-feature-name
   ```

## Development Workflow

### 1. Code Organization

- Keep files focused and single-purpose
- Follow the established project structure:
  ```
  backend/
  ├── app/          # Main application code
  ├── src/          # Core business logic
  ├── tests/        # Test files
  └── README.md     # Component documentation
  ```

### 2. Commit Standards

Follow the conventional commits specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

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

### 3. Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch
- Feature branches: `feature/123-feature-name`
- Bug fixes: `fix/123-bug-name`
- Hotfixes: `hotfix/123-issue-name`

## Code Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use type hints
- Maximum line length: 88 characters (Black formatter)
- Use docstrings for all public functions and classes

### Documentation Requirements

- All new features must include:
  - Technical documentation
  - Usage examples
  - API documentation (if applicable)
  - Updated README (if applicable)

### Testing Requirements

- Maintain minimum 80% code coverage
- Include unit tests for new features
- Include integration tests for API endpoints
- Test edge cases and error conditions

## Pull Request Process

1. **Before Submitting**

   - Update documentation
   - Add/update tests
   - Run linters and formatters
   - Update CHANGELOG.md

2. **PR Requirements**

   - Fill out the PR template completely
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

   - Create release branch
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

## Additional Resources

- [Documentation Standards](docs/DOCUMENTATION_STANDARDS.md)
- [Git Workflow](docs/GIT_WORKFLOW.md)
- [Architecture Overview](docs/ARCHITECTURE.md)

## Questions and Support

- Open an issue with the "question" label
- Tag relevant maintainers
- Check existing documentation first
- Join our community discussions

## License

By contributing, you agree that your contributions will be licensed under the project's license.
