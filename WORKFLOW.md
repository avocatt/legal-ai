# Development Workflow

This document outlines the standardized development process for the Turkish Legal AI Assistant project.

## Request Format

When requesting changes, use the following format:
```
action: <action_type>
description: <detailed_description>
scope: <affected_components>
```

Where:
- `action_type`: Type of change being made
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation changes
  - `refactor`: Code refactoring
  - `test`: Adding/modifying tests
  - `style`: Code style/formatting changes
  - `chore`: Maintenance tasks
- `description`: Detailed description of what needs to be done
- `scope`: Which part of the project is affected (e.g., backend/rag, frontend, etc.)

Example:
```
action: feat
description: Add temperature parameter to QA chain for controlling response creativity
scope: backend/rag
```

## Development Process

### 1. Analysis Phase
The AI assistant will respond with:
```
ANALYSIS
- Purpose: <why we're making this change>
- Files to modify: <list of files>
- Proposed changes: <detailed changes>

Do you want me to proceed with these changes? (y/n)
```

### 2. Implementation Phase
After approval, the AI will:
- Show changes being made
- Explain each significant change
- Use appropriate tool calls to implement changes

### 3. Testing Phase
The AI will:
- Create/modify relevant tests
- Run the test suite
- Show test results
- Ensure all tests pass

### 4. Commit and Push Phase
The AI will propose a commit with:
```
<type>(<scope>): <summary>

<description>

Changes:
- <detailed list of changes>

Tests:
- <list of tests added/modified>
- <test results>

Shall I commit these changes? (y/n)
```

After commit approval, the AI will automatically:
1. Execute the commit
2. Push to the current branch
3. Show push results

## Commit Message Standards

1. Format:
```
<type>(<scope>): <summary>

<description>

- Detailed changes:
  * Change 1
  * Change 2
  
Tests:
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing

Related: #issue_number
```

2. Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semi colons, etc.
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

3. Scope:
- `rag`: RAG system components
- `api`: API endpoints
- `frontend`: Frontend changes
- `tools`: Development tools
- `root`: Project-level changes

## Example Complete Workflow

1. Request:
```
action: feat
description: Add new prompt template for legal questions
scope: backend/rag
```

2. Analysis Response:
```
ANALYSIS
- Purpose: Improve question handling with specialized prompt
- Files to modify: 
  * backend/src/rag/prompts/templates.py
  * backend/tests/test_prompts.py
- Proposed changes: Add new template and tests

Do you want me to proceed with these changes? (y/n)
```

3. Implementation & Testing:
```
IMPLEMENTATION
- Adding new prompt template
- Updating tests
- Running test suite

TESTING
- New tests added for prompt template
- All tests passing
```

4. Commit and Push:
```
feat(rag): add specialized legal question prompt template

- Add new prompt template for legal questions
- Improve response structure
- Add comprehensive tests

Changes:
- Added new template in templates.py
- Updated test suite

Tests:
- Added template validation tests
- Added response format tests
- All tests passing

Shall I commit these changes? (y/n)
```

After approval:
```
[restore-documentation abc1234] feat(rag): add specialized legal question prompt template
 2 files changed, 45 insertions(+), 0 deletions(-)

Pushing changes to current branch...
To github.com:username/legal-ai.git
   def5678..abc1234  restore-documentation -> restore-documentation
``` 