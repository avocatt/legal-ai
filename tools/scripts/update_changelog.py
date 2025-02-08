#!/usr/bin/env python3
"""Update CHANGELOG.md with new changes from git commits.

This script updates the CHANGELOG.md file by:
1. Getting the latest version from CHANGELOG.md
2. Getting commit messages since that version
3. Categorizing commits into types (Added, Changed, Fixed, etc.)
4. Adding a new unreleased section with the changes
"""

import os
import re
import subprocess
from typing import Dict, List, Optional, Tuple

CHANGELOG_PATH = "CHANGELOG.md"
UNRELEASED_PATTERN = r"\[Unreleased\]"
VERSION_PATTERN = r"\[(\d+\.\d+\.\d+)\]"
GIT_LOG_FMT = "%s"  # Simple format for commit messages

# Commit type mappings
TYPE_MAPPINGS = {
    "feat": "Added",
    "feature": "Added",
    "add": "Added",
    "fix": "Fixed",
    "docs": "Changed",
    "style": "Changed",
    "refactor": "Changed",
    "perf": "Changed",
    "test": "Changed",
    "chore": "Changed",
    "remove": "Removed",
    "delete": "Removed",
}


def parse_commit_message(message: str) -> Tuple[str, str]:
    """Parse conventional commit message.

    Format: type(scope): description
    Example: feat(api): add new endpoint
    """
    # Match conventional commit format
    match = re.match(r"^(\w+)(?:\(([^)]+)\))?: (.+)$", message)
    if match:
        type_, scope, desc = match.groups()
        # Clean up description
        desc = desc.strip()
        if scope:
            desc = f"{scope}: {desc}"
        return type_.lower(), desc
    return "other", message


def get_latest_version() -> Optional[str]:
    """Get the latest version from CHANGELOG.md."""
    if not os.path.exists(CHANGELOG_PATH):
        return None

    with open(CHANGELOG_PATH, "r") as f:
        content = f.read()

    versions = re.findall(VERSION_PATTERN, content)
    return versions[0] if versions else None


def get_commit_messages() -> List[str]:
    """Get commit messages since the last version."""
    latest_version = get_latest_version()
    git_cmd = ["git", "log", f"--pretty=format:{GIT_LOG_FMT}"]

    if latest_version:
        git_cmd.append(f"v{latest_version}..HEAD")

    result = subprocess.run(git_cmd, capture_output=True, text=True)
    return result.stdout.splitlines()


def categorize_commits(commits: List[str]) -> Dict[str, List[str]]:
    """Categorize commits by type (Added, Changed, Fixed, etc.)."""
    categories = {"Added": [], "Changed": [], "Fixed": [], "Removed": []}

    for commit in commits:
        type_, desc = parse_commit_message(commit)
        category = TYPE_MAPPINGS.get(type_, "Changed")
        if desc not in categories[category]:  # Avoid duplicates
            categories[category].append(desc)

    return {k: v for k, v in categories.items() if v}


def update_changelog(categories: Dict[str, List[str]]) -> None:
    """Update CHANGELOG.md with new changes."""
    if not os.path.exists(CHANGELOG_PATH):
        print(f"Creating new {CHANGELOG_PATH}")
        header = "# Changelog\n\n"
        desc = (
            "All notable changes to this project will be documented in this file.\n\n"
            "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),\n"
            "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n"
        )
        initial = "## [Unreleased]\n"
        with open(CHANGELOG_PATH, "w") as f:
            f.write(header + desc + initial)

    with open(CHANGELOG_PATH, "r") as f:
        content = f.read()

    # Remove existing unreleased section if it exists
    pattern = rf"{UNRELEASED_PATTERN}.*?(?=##|$)"
    content = re.sub(pattern, "", content, flags=re.DOTALL)

    # Add new unreleased section
    unreleased = "## [Unreleased]\n\n"
    for category, commits in categories.items():
        if commits:
            unreleased += f"### {category}\n\n"
            for commit in commits:
                unreleased += f"- {commit}\n"
            unreleased += "\n"

    # Insert unreleased section after header
    header_end = content.find("\n## ")
    if header_end == -1:
        header_end = len(content)
    content = content[:header_end] + unreleased + content[header_end:]

    with open(CHANGELOG_PATH, "w") as f:
        f.write(content.strip() + "\n")


def main() -> None:
    """Run the changelog update process."""
    commits = get_commit_messages()
    if not commits:
        print("No new commits found.")
        return

    categories = categorize_commits(commits)
    if not categories:
        print("No categorizable changes found.")
        return

    update_changelog(categories)
    print("Successfully updated CHANGELOG.md")


if __name__ == "__main__":
    main()
