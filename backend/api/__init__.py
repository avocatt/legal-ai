"""API package for Turkish Legal AI."""

from .config import Settings, get_settings
from .routes import router

__all__ = ["Settings", "get_settings", "router"]
