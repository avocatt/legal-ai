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
from typing import Dict, List, Optional

CHANGELOG_PATH = "CHANGELOG.md"
UNRELEASED_PATTERN = r"\[Unreleased\]"
VERSION_PATTERN = r"\[(\d+\.\d+\.\d+)\]"
GIT_LOG_FMT = "%s"  # Simple format for commit messages


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
    categories = {"Added": [], "Changed": [], "Fixed": [], "Removed": [], "Other": []}

    for commit in commits:
        if commit.startswith("feat"):
            categories["Added"].append(commit)
        elif commit.startswith(("refactor", "style")):
            categories["Changed"].append(commit)
        elif commit.startswith("fix"):
            categories["Fixed"].append(commit)
        elif commit.startswith("remove"):
            categories["Removed"].append(commit)
        else:
            categories["Other"].append(commit)

    return {k: v for k, v in categories.items() if v}


def update_changelog(categories: Dict[str, List[str]]) -> None:
    """Update CHANGELOG.md with new changes."""
    if not os.path.exists(CHANGELOG_PATH):
        print(f"Creating new {CHANGELOG_PATH}")
        header = "# Changelog\n\n"
        desc = (
            "All notable changes to this project will be documented "
            "in this file.\n\n"
        )
        initial = "[Unreleased]\n"

        with open(CHANGELOG_PATH, "w") as f:
            f.write(header + desc + initial)

    with open(CHANGELOG_PATH, "r") as f:
        content = f.read()

    # Remove existing unreleased section if it exists
    pattern = rf"{UNRELEASED_PATTERN}.*?(?=\[|$)"
    content = re.sub(pattern, "", content, flags=re.DOTALL)

    # Add new unreleased section
    unreleased = "[Unreleased]\n"
    for category, commits in categories.items():
        if commits:
            unreleased += f"\n### {category}\n"
            for commit in commits:
                unreleased += f"- {commit}\n"

    # Insert unreleased section after header
    header_end = content.find("\n\n") + 2
    content = content[:header_end] + unreleased + "\n" + content[header_end:]

    with open(CHANGELOG_PATH, "w") as f:
        f.write(content.strip() + "\n")


def main() -> None:
    """Run the changelog update process."""
    commits = get_commit_messages()
    if not commits:
        print("No new commits found.")
        return

    categories = categorize_commits(commits)
    update_changelog(categories)
    print("Successfully updated CHANGELOG.md")


if __name__ == "__main__":
    main()
