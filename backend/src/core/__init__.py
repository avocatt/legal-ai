"""Core functionality module for the Turkish Legal AI system."""

from .config import Settings, get_settings
from .logging import setup_logging, get_logger, LoggerMixin

__all__ = [
    "Settings",
    "get_settings",
    "setup_logging",
    "get_logger",
    "LoggerMixin",
]
