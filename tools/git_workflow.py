#!/usr/bin/env python3
"""Automated Git Workflow Script.

This script automates the git workflow process from staging changes to creating pull requests.
It enforces conventional commits and project standards throughout the process.
"""

import argparse
import subprocess
import sys
from typing import List, Optional, Tuple


class GitWorkflow:
    """Handles the automated git workflow process including commits and pull requests."""

    def __init__(self):
        """Initialize GitWorkflow with current branch information."""
        self.current_branch = self.get_current_branch()

    def run_command(
        self, command: List[str], check: bool = True
    ) -> Tuple[int, str, str]:
        """Run a shell command and return exit code, stdout, and stderr."""
        try:
            result = subprocess.run(
                command,
                check=check,
                text=True,
                capture_output=True,
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout, e.stderr

    def get_current_branch(self) -> str:
        """Get the name of the current git branch."""
        code, stdout, _ = self.run_command(["git", "branch", "--show-current"])
        return stdout.strip() if code == 0 else ""

    def run_pre_commit(self) -> bool:
        """Run pre-commit checks."""
        print("\n🔍 Running pre-commit checks...")
        code, stdout, stderr = self.run_command(
            ["pre-commit", "run", "--all-files"], check=False
        )
        print(stdout)
        if code != 0:
            print("❌ Pre-commit checks failed. Please fix the issues and try again.")
            if stderr:
                print(f"Error: {stderr}")
            return False
        print("✅ Pre-commit checks passed!")
        return True

    def stage_changes(self, files: Optional[List[str]] = None) -> bool:
        """Stage changes for commit."""
        print("\n📦 Staging changes...")
        if files:
            for file in files:
                code, _, stderr = self.run_command(["git", "add", file])
                if code != 0:
                    print(f"❌ Failed to stage {file}: {stderr}")
                    return False
        else:
            code, _, stderr = self.run_command(["git", "add", "."])
            if code != 0:
                print(f"❌ Failed to stage changes: {stderr}")
                return False
        print("✅ Changes staged successfully!")
        return True

    def commit_changes(
        self, type: str, scope: str, description: str, body: Optional[str] = None
    ) -> bool:
        """Create a commit with conventional commit format."""
        print("\n💾 Creating commit...")
        commit_msg = f"{type}"
        if scope:
            commit_msg += f"({scope})"
        commit_msg += f": {description}"

        if body:
            commit_msg += f"\n\n{body}"

        code, _, stderr = self.run_command(["git", "commit", "-m", commit_msg])
        if code != 0:
            print(f"❌ Failed to create commit: {stderr}")
            return False
        print("✅ Changes committed successfully!")
        return True

    def push_changes(self) -> bool:
        """Push changes to remote repository."""
        print("\n⬆️ Pushing changes to remote...")
        code, _, stderr = self.run_command(
            ["git", "push", "origin", self.current_branch]
        )
        if code != 0:
            print(f"❌ Failed to push changes: {stderr}")
            return False
        print("✅ Changes pushed successfully!")
        return True

    def create_pull_request(
        self, title: str, body: str, base_branch: str = "develop"
    ) -> bool:
        """Create a pull request using gh cli."""
        print("\n🔄 Creating pull request...")

        # Check if gh cli is installed
        code, _, _ = self.run_command(["gh", "--version"], check=False)
        if code != 0:
            print("❌ GitHub CLI (gh) is not installed. Please install it first:")
            print("  brew install gh  # For macOS")
            print("  Or visit: https://cli.github.com/")
            return False

        code, _, stderr = self.run_command(
            [
                "gh",
                "pr",
                "create",
                "--title",
                title,
                "--body",
                body,
                "--base",
                base_branch,
                "--head",
                self.current_branch,
            ]
        )
        if code != 0:
            print(f"❌ Failed to create pull request: {stderr}")
            return False
        print("✅ Pull request created successfully!")
        return True


def main():
    """Execute the git workflow automation process."""
    parser = argparse.ArgumentParser(description="Automated Git Workflow")
    parser.add_argument(
        "--type", required=True, help="Commit type (feat, fix, docs, etc.)"
    )
    parser.add_argument("--scope", default="", help="Commit scope")
    parser.add_argument("--description", required=True, help="Commit description")
    parser.add_argument("--body", help="Commit body")
    parser.add_argument("--files", nargs="+", help="Specific files to commit")
    parser.add_argument("--base", default="develop", help="Base branch for PR")
    parser.add_argument(
        "--skip-pr", action="store_true", help="Skip pull request creation"
    )

    args = parser.parse_args()

    workflow = GitWorkflow()

    # Run the workflow
    if not workflow.run_pre_commit():
        sys.exit(1)

    if not workflow.stage_changes(args.files):
        sys.exit(1)

    if not workflow.commit_changes(args.type, args.scope, args.description, args.body):
        sys.exit(1)

    if not workflow.push_changes():
        sys.exit(1)

    if not args.skip_pr:
        pr_title = (
            f"{args.type}({args.scope}): {args.description}"
            if args.scope
            else f"{args.type}: {args.description}"
        )
        pr_body = f"""## Changes Made
{args.body if args.body else args.description}

## Checklist
- [x] Code follows project style guidelines
- [x] Tests added/updated (if applicable)
- [x] Documentation updated (if applicable)
- [x] Pre-commit hooks passed
- [x] CHANGELOG.md updated (if applicable)
"""
        if not workflow.create_pull_request(pr_title, pr_body, args.base):
            sys.exit(1)

    print("\n✨ Workflow completed successfully!")


if __name__ == "__main__":
    main()
