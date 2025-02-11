"""Data store package for Turkish Legal AI."""

from .criminal_code_store import CriminalCodeVectorizer
from .legal_terms_store import LegalTermsVectorizer
from .embeddings import get_embeddings_model

__all__ = ["CriminalCodeVectorizer",
           "LegalTermsVectorizer", "get_embeddings_model"]
