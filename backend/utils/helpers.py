"""Provide helper functions for the Turkish Legal AI system."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Union

from api.config import get_settings


def ensure_directory(path: str) -> None:
    """Ensure a directory exists, create if it doesn't."""
    Path(path).mkdir(parents=True, exist_ok=True)


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


def get_data_dir() -> Path:
    """Get the data directory path."""
    data_dir = get_project_root() / "data"
    ensure_directory(str(data_dir))
    return data_dir


def validate_api_keys() -> None:
    """Validate that necessary API keys are present."""
    settings = get_settings()

    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    if not settings.HUGGINGFACE_TOKEN:
        print("Warning: HUGGINGFACE_TOKEN not found. Some features may be slower.")


def load_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load and parse a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Dict[str, Any]: Parsed JSON content

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """Save data to a JSON file.

    Args:
        data: Data to save
        file_path: Path where to save the file

    Raises:
        IOError: If there's an error writing the file
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
