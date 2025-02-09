# Pull Request Template

## Request Format

When requesting a pull request creation, use the following format:
```
action: pr
type: <pr_type>
title: <pr_title>
description: <detailed_description>
related_issue: <issue_number>  # Optional
```

Where:
- `pr_type`: Type of changes
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation changes
  - `refactor`: Code refactoring
  - `test`: Testing changes
  - `style`: Code style changes
  - `chore`: Maintenance
- `title`: Brief, descriptive title
- `description`: Detailed explanation of changes
- `related_issue`: Issue number if applicable

Example:
```
action: pr
type: feat
title: Add temperature control to QA chain
description: Implement temperature parameter in the QA chain to control response creativity
related_issue: 123
```

## AI Response Format

The AI will create a pull request with:

### 1. Pull Request Content

```
# Pull Request

## Description
[Detailed description from the request]

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

## Documentation
- [ ] README.md updated (if needed)
- [ ] Documentation updated
- [ ] Code comments updated

## Checklist
- [ ] Code follows project's style guidelines
- [ ] Self-review performed
- [ ] Code commented in complex areas
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added and passing
- [ ] Dependencies updated if needed

## Changes Made
[List of specific changes made]

## Test Results
[Summary of test results]
```

### 2. Branch Information
```
Source Branch: feature/[feature-name]
Target Branch: main
```

### 3. Review Instructions
```
Key areas to review:
- [Specific files or changes to focus on]
- [Important implementation details]
- [Testing considerations]
```

## Example Usage

Request:
```
action: pr
type: feat
title: Implement specialized legal prompt templates
description: Add new prompt templates optimized for different types of legal questions
related_issue: 45
```

AI Response:
```
Creating pull request...

Branch: feature/legal-prompt-templates
Target: main

# Pull Request

## Description
Add new prompt templates optimized for different types of legal questions...

[Rest of the PR content following the template above]
``` 