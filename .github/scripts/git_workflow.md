# Git Workflow Automation Tool

This tool automates the entire git workflow process from staging changes to creating pull requests, following our project's conventions and standards.

## Prerequisites

1. Python 3.6+
2. Git
3. GitHub CLI (`gh`) - For pull request creation
4. Pre-commit hooks installed

## Installation

1. Install GitHub CLI:

   ```bash
   # For macOS
   brew install gh

   # Then authenticate
   gh auth login
   ```

2. Ensure the script is executable:
   ```bash
   chmod +x tools/git_workflow.py
   ```

## Usage

Basic usage:

```bash
./tools/git_workflow.py --type TYPE --description "Your commit message"
```

Full options:

```bash
./tools/git_workflow.py \
  --type TYPE \            # Required: commit type (feat, fix, docs, etc.)
  --scope SCOPE \         # Optional: commit scope
  --description "DESC" \  # Required: commit description
  --body "BODY" \        # Optional: detailed description
  --files FILE1 FILE2 \  # Optional: specific files to commit
  --base BRANCH \        # Optional: base branch for PR (default: develop)
  --skip-pr             # Optional: skip PR creation
```

### Examples

1. Simple documentation change:

   ```bash
   ./tools/git_workflow.py --type docs --description "update README with new features"
   ```

2. Feature with scope and body:

   ```bash
   ./tools/git_workflow.py \
     --type feat \
     --scope api \
     --description "add user authentication endpoint" \
     --body "- Added JWT authentication
     - Implemented refresh tokens
     - Added rate limiting"
   ```

3. Commit specific files:
   ```bash
   ./tools/git_workflow.py \
     --type fix \
     --description "fix CORS issues" \
     --files backend/app/main.py backend/app/config.py
   ```

## Features

1. **Pre-commit Checks**

   - Runs all pre-commit hooks
   - Provides clear error messages

2. **Conventional Commits**

   - Enforces conventional commit format
   - Supports all standard types and scopes

3. **Automated PR Creation**

   - Creates standardized PR titles
   - Includes default checklist
   - Links to related issues

4. **Error Handling**
   - Clear error messages
   - Proper exit codes
   - Rollback on failure

## Workflow Steps

1. Runs pre-commit checks
2. Stages specified files (or all changes)
3. Creates a conventional commit
4. Pushes to remote repository
5. Creates a pull request (unless --skip-pr is used)

## Troubleshooting

1. **Pre-commit Fails**

   - Check the error message
   - Fix the issues
   - Run the script again

2. **PR Creation Fails**

   - Ensure GitHub CLI is installed and authenticated
   - Check if branch exists on remote
   - Verify you have proper permissions

3. **Push Fails**
   - Pull latest changes
   - Resolve any conflicts
   - Try again

## Contributing

Feel free to suggest improvements or report issues with this script in our issue tracker.
