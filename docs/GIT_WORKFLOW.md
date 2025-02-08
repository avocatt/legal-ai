# Git Workflow

## Branch Strategy

### Main Branches

- `main` - Production-ready code
- `develop` - Integration branch for features

### Feature Branches

Format: `feature/[issue-number]-brief-description`
Example: `feature/123-add-authentication`

### Bug Fix Branches

Format: `fix/[issue-number]-brief-description`
Example: `fix/124-cors-error`

### Release Branches

Format: `release/vX.Y.Z`
Example: `release/v1.2.0`

### Hotfix Branches

Format: `hotfix/[issue-number]-brief-description`
Example: `hotfix/125-critical-security-fix`

## Workflow

1. **Start New Work**

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/123-add-authentication
   ```

2. **Regular Development**

   ```bash
   git add .
   git commit -m "feat: add user authentication system"
   git push origin feature/123-add-authentication
   ```

3. **Create Pull Request**

   - Create PR from feature branch to `develop`
   - Fill out PR template
   - Request reviews
   - Address feedback

4. **Merge to Develop**

   - Squash and merge to keep history clean
   - Delete feature branch after merge

5. **Release Process**

   ```bash
   git checkout develop
   git checkout -b release/v1.2.0
   # Make release-specific changes
   git push origin release/v1.2.0
   ```

6. **Hotfix Process**
   ```bash
   git checkout main
   git checkout -b hotfix/125-critical-security-fix
   # Fix the issue
   git push origin hotfix/125-critical-security-fix
   ```

## Commit Message Convention

Format: `<type>(<scope>): <description>`

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

### Scopes

- `backend`
- `frontend`
- `docs`
- `data`
- `rag`
- `ci`
- `deps`

### Examples

```
feat(backend): add user authentication system
fix(frontend): resolve CORS issues in API calls
docs(readme): update installation instructions
style(frontend): format components using prettier
refactor(rag): improve prompt template structure
test(backend): add tests for QA chain
chore(deps): update dependencies
```

## Pull Request Template

```markdown
## Description

[Describe the changes made in this PR]

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues

Fixes #[issue number]

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Checklist

- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] CHANGELOG.md updated
- [ ] All checks passing
```

## Branch Protection Rules

### `main` Branch

- Require pull request reviews
- Require status checks to pass
- No direct pushes
- No force pushes

### `develop` Branch

- Require pull request reviews
- Require status checks to pass
- No direct pushes
- Allow force pushes with lease

### Feature/Fix Branches

- No special protection
- Delete after merge

## Initial Setup

To transition to this workflow:

1. Create develop branch:

   ```bash
   git checkout main
   git checkout -b develop
   git push origin develop
   ```

2. Set up branch protection:

   - Go to repository settings
   - Add protection rules for main and develop

3. Update local repositories:

   ```bash
   git fetch origin
   git checkout develop
   ```

4. Start using feature branches:
   ```bash
   git checkout develop
   git checkout -b feature/[issue-number]-description
   ```

## Best Practices

1. **Keep Branches Updated**

   ```bash
   git checkout develop
   git pull origin develop
   git checkout feature/123-add-authentication
   git rebase develop
   ```

2. **Clean Commits**

   - Write meaningful commit messages
   - Squash related commits
   - Keep commits focused

3. **Code Review**

   - Review all changes thoroughly
   - Use PR templates
   - Address all comments

4. **Documentation**

   - Update docs with code changes
   - Keep CHANGELOG.md current
   - Document breaking changes

5. **Testing**
   - Run tests before pushing
   - Add tests for new features
   - Update existing tests
