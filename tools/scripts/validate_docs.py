#!/usr/bin/env python3
"""Validate project documentation against established standards.

This script checks:
1. README.md for required sections
2. CHANGELOG.md for proper format
3. Component documentation for completeness
4. API documentation for required files
"""

import os
import re
from typing import Dict, List

DOCS_STANDARDS_PATH = "docs/DOCUMENTATION_STANDARDS.md"
REQUIRED_README_SECTIONS = {
    "Overview",
    "Quick Start",
    "Documentation",
    "Development",
    "Contributing",
}


def load_doc_standards() -> Dict[str, List[str]]:
    """Load documentation standards from DOCUMENTATION_STANDARDS.md."""
    if not os.path.exists(DOCS_STANDARDS_PATH):
        print(f"Warning: {DOCS_STANDARDS_PATH} not found")
        return {}

    with open(DOCS_STANDARDS_PATH, "r") as f:
        content = f.read()

    standards = {}
    current_section = None

    for line in content.split("\n"):
        if line.startswith("## "):
            current_section = line[3:].strip()
            standards[current_section] = []
        elif current_section and line.startswith("- "):
            standards[current_section].append(line[2:].strip())

    return standards


def validate_readme(path: str) -> bool:
    """Validate README.md content and structure."""
    if not os.path.exists(path):
        print(f"Error: {path} not found")
        return False

    with open(path, "r") as f:
        content = f.read()

    # Check for required sections
    found_sections = set()
    for section in REQUIRED_README_SECTIONS:
        pattern = rf"^## {section}$"
        if re.search(pattern, content, re.MULTILINE):
            found_sections.add(section)

    missing = REQUIRED_README_SECTIONS - found_sections
    if missing:
        print(f"Missing required sections in {path}:")
        for section in missing:
            print(f"- {section}")
        return False

    # Check for implementation status
    if "## Implementation Status" not in content:
        print(f"Missing Implementation Status section in {path}")
        return False

    # Check for badges
    if not re.search(r"!\[.*?\]\(.*?\)", content):
        print(f"Warning: No badges found in {path}")

    return True


def validate_changelog(path: str) -> bool:
    """Validate CHANGELOG.md format and content."""
    if not os.path.exists(path):
        print(f"Error: {path} not found")
        return False

    with open(path, "r") as f:
        content = f.read()

    # Check for Unreleased section
    if "[Unreleased]" not in content:
        print(f"Missing [Unreleased] section in {path}")
        return False

    # Check version entries format
    version_pattern = r"\[\d+\.\d+\.\d+\]"
    if not re.search(version_pattern, content):
        print(f"No version entries found in {path}")
        return False

    # Check for change categories
    categories = ["Added", "Changed", "Fixed", "Removed"]
    found_categories = [cat for cat in categories if f"### {cat}" in content]
    if not found_categories:
        print(f"No change categories found in {path}")
        return False

    return True


def validate_component_docs(path: str) -> bool:
    """Validate component-level documentation."""
    if not os.path.exists(path):
        return True  # Skip if directory doesn't exist

    readme_path = os.path.join(path, "README.md")
    if not os.path.exists(readme_path):
        print(f"Missing README.md in {path}")
        return False

    with open(readme_path, "r") as f:
        content = f.read()

    required_sections = ["Overview", "Usage", "Configuration"]
    missing = []
    for section in required_sections:
        if f"## {section}" not in content:
            missing.append(section)

    if missing:
        print(f"Missing sections in {readme_path}:")
        for section in missing:
            print(f"- {section}")
        return False

    return True


def validate_api_docs(path: str) -> bool:
    """Validate API documentation completeness."""
    api_dir = os.path.join(path, "api")
    if not os.path.exists(api_dir):
        print("Missing API documentation directory")
        return False

    required_files = ["overview.md", "endpoints.md", "models.md"]
    missing = []
    for file in required_files:
        if not os.path.exists(os.path.join(api_dir, file)):
            missing.append(file)

    if missing:
        print("Missing API documentation files:")
        for file in missing:
            print(f"- {file}")
        return False

    return True


def main() -> None:
    """Run documentation validation checks."""
    success = True
    success &= validate_readme("README.md")
    success &= validate_changelog("CHANGELOG.md")
    success &= validate_component_docs("frontend")
    success &= validate_component_docs("backend")
    success &= validate_api_docs("docs")

    if success:
        print("All documentation checks passed!")
    else:
        print("Some documentation checks failed.")
        exit(1)


if __name__ == "__main__":
    main()
