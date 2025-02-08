#!/usr/bin/env python3
"""Update README.md with current project status and documentation links.

This script updates the README.md file by:
1. Checking implementation status of core features
2. Updating documentation links
3. Reflecting current project state
"""

import os
import re
from pathlib import Path
from typing import Dict

README_PATH = "README.md"
ROADMAP_PATH = "ROADMAP.md"

# Core features with their corresponding paths
CORE_FEATURES = {
    "RAG System": "backend/src/rag/rag_system.py",
    "Frontend UI": "frontend/src/App.tsx",
    "Backend API": "backend/app/main.py",
    "Data Processing": "tools/data_processing",
}

# Regex patterns for section matching
STATUS_START = r"## Implementation Status\n\n"
STATUS_END = r"(?:- [^\n]+\n)+"
DOCS_START = r"## Documentation\n\n"
DOCS_END = r"(?:- \[[^\]]+\]\([^)]+\)\n)+"


def get_implementation_status() -> Dict[str, bool]:
    """Check implementation status of core features."""
    status = {}
    for feature, path in CORE_FEATURES.items():
        status[feature] = os.path.exists(path)
    return status


def update_implementation_status() -> None:
    """Update implementation status section in README.md."""
    if not os.path.exists(README_PATH):
        print(f"Error: {README_PATH} not found")
        return

    status = get_implementation_status()

    with open(README_PATH, "r") as f:
        content = f.read()

    # Create implementation status section
    status_section = "## Implementation Status\n\n"
    for feature, implemented in status.items():
        icon = "✅" if implemented else "🚧"
        status_section += f"- {icon} {feature}\n"

    # Update or add implementation status section
    status_pattern = STATUS_START + STATUS_END

    if re.search(status_pattern, content):
        content = re.sub(status_pattern, status_section, content)
    else:
        # Add after project description
        desc_end = content.find("\n## ")
        if desc_end == -1:
            desc_end = len(content)

        parts = [content[:desc_end], "\n\n", status_section, content[desc_end:]]
        content = "".join(parts)

    with open(README_PATH, "w") as f:
        f.write(content)


def update_documentation_links() -> None:
    """Update documentation links section in README.md."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        return

    doc_files = []
    for ext in ["*.md", "*.rst"]:
        doc_files.extend(docs_dir.glob(ext))

    if not doc_files:
        return

    with open(README_PATH, "r") as f:
        content = f.read()

    # Create documentation links section
    docs_section = "## Documentation\n\n"
    for doc_file in sorted(doc_files):
        name = doc_file.stem.replace("_", " ").title()
        path = doc_file.as_posix()
        docs_section += f"- [{name}]({path})\n"

    # Update or add documentation links section
    docs_pattern = DOCS_START + DOCS_END

    if re.search(docs_pattern, content):
        content = re.sub(docs_pattern, docs_section, content)
    else:
        # Add after implementation status
        impl_section = "## Implementation"
        impl_start = content.find(impl_section)
        impl_end = content.find("\n## ", impl_start)
        if impl_end == -1:
            impl_end = len(content)

        parts = [content[:impl_end], "\n\n", docs_section, content[impl_end:]]
        content = "".join(parts)

    with open(README_PATH, "w") as f:
        f.write(content)


def main() -> None:
    """Run the README update process."""
    update_implementation_status()
    update_documentation_links()
    print("Successfully updated README.md")


if __name__ == "__main__":
    main()
