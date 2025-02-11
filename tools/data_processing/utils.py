"""Shared utilities for data processing scripts."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def ensure_directory(path: str) -> None:
    """Ensure a directory exists, create if it doesn't."""
    Path(path).mkdir(parents=True, exist_ok=True)


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def get_data_dir() -> Path:
    """Get the data directory path."""
    data_dir = get_project_root() / "data"
    ensure_directory(str(data_dir))
    return data_dir


def save_json(data: Any, file_path: str, ensure_dir: bool = True) -> None:
    """Save data to JSON file."""
    if ensure_dir:
        ensure_directory(os.path.dirname(file_path))

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(file_path: str) -> Dict:
    """Load data from JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_dataframe(df: pd.DataFrame, file_path: str, ensure_dir: bool = True) -> None:
    """Save DataFrame to CSV file."""
    if ensure_dir:
        ensure_directory(os.path.dirname(file_path))

    df.to_csv(file_path, index=False, encoding="utf-8")


def load_dataframe(file_path: str) -> pd.DataFrame:
    """Load DataFrame from CSV file."""
    return pd.read_csv(file_path, encoding="utf-8")
