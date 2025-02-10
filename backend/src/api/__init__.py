"""API module for the Turkish Legal AI system."""

from .endpoints.qa import router as qa_router

__all__ = ["qa_router"]
