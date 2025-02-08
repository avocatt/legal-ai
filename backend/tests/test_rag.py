"""Tests for the Turkish Legal RAG system."""

import pytest
from src.rag import TurkishLegalRAG

# Test data
TEST_LAW_JSON = "tests/data/test_law.json"
TEST_TERMS_JSON = "tests/data/test_terms.json"


def test_rag_initialization():
    """Test RAG system initialization."""
    with pytest.raises(FileNotFoundError):
        # Should raise error for non-existent file
        TurkishLegalRAG("non_existent_file.json")


def test_retrieval():
    """Test document retrieval."""
    rag = TurkishLegalRAG("data/processed/processed_law.json")

    # Test with valid query
    results = rag.retrieve("ceza kanunu")
    assert len(results) > 0
    assert all(isinstance(r, dict) for r in results)

    # Test with empty query
    with pytest.raises(ValueError):
        rag.retrieve("")

    # Test with invalid query type
    with pytest.raises(ValueError):
        rag.retrieve(123)


def test_metadata_filtering():
    """Test metadata filtering in retrieval."""
    rag = TurkishLegalRAG("data/processed/processed_law.json")

    # Test with valid metadata filter
    results = rag.retrieve("ceza", metadata_filter={"book": "İKİNCİ KİTAP"})
    assert all(r["metadata"]["book"] == "İKİNCİ KİTAP" for r in results)

    # Test with invalid metadata filter
    with pytest.raises(ValueError):
        rag.retrieve("ceza", metadata_filter="invalid")


def test_context_formatting():
    """Test context formatting."""
    rag = TurkishLegalRAG("data/processed/processed_law.json")

    # Get some results
    results = rag.retrieve("ceza")

    # Test context formatting
    context = rag.format_context(results)
    assert isinstance(context, str)
    assert len(context) > 0


# Add more tests as needed
