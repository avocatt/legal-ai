"""
Turkish Legal RAG system package.
"""

from .embeddings import get_embedding_function
from .retriever import DocumentRetriever
from .qa_chain import LegalQAChain

# For backward compatibility
TurkishLegalRAG = DocumentRetriever

__all__ = ['DocumentRetriever', 'LegalQAChain', 'get_embedding_function', 'TurkishLegalRAG']
