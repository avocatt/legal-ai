"""API package for the Turkish Legal AI system."""

from .routes import router as qa_router, Question, Answer, SearchResult

__all__ = [
    "qa_router",
    "Question",
    "Answer",
    "SearchResult",
]
