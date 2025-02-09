"""Tests for the Turkish Legal RAG system."""

import os
import pytest
from src.rag import TurkishLegalRAG

# Test data paths
TEST_LAW_JSON = "tests/data/processed/criminal_law/processed_law.json"
TEST_TERMS_JSON = "tests/data/processed/legal_terms/legal_terms.json"


@pytest.fixture(autouse=True)
def cleanup_collections():
    """Clean up test collections before and after each test."""
    import chromadb
    client = chromadb.Client()
    try:
        client.delete_collection("turkish_criminal_law")
        client.delete_collection("turkish_legal_terms")
    except ValueError:
        pass
    yield
    try:
        client.delete_collection("turkish_criminal_law")
        client.delete_collection("turkish_legal_terms")
    except ValueError:
        pass


def test_rag_initialization():
    """Test RAG system initialization."""
    with pytest.raises(FileNotFoundError):
        # Should raise error for non-existent files
        TurkishLegalRAG(
            law_json_path="non_existent_file.json",
            terms_json_path="non_existent_terms.json"
        )


def test_retrieval():
    """Test document retrieval."""
    rag = TurkishLegalRAG(
        law_json_path=TEST_LAW_JSON,
        terms_json_path=TEST_TERMS_JSON
    )

    # Test with valid query
    results = rag.retrieve("ceza")
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
    rag = TurkishLegalRAG(
        law_json_path=TEST_LAW_JSON,
        terms_json_path=TEST_TERMS_JSON
    )

    # Test with valid metadata filter
    results = rag.retrieve("ceza", metadata_filter={"type": "article"})
    assert len(results) > 0
    assert all(r["metadata"]["type"] == "article" for r in results)

    # Test filtering by book
    results = rag.retrieve("ceza", metadata_filter={"book": "BİRİNCİ KİTAP"})
    assert len(results) > 0
    assert all(r["metadata"]["book"] == "BİRİNCİ KİTAP" for r in results)

    # Test with invalid metadata filter
    with pytest.raises(ValueError):
        rag.retrieve("ceza", metadata_filter="invalid")


def test_context_formatting():
    """Test context formatting."""
    rag = TurkishLegalRAG(
        law_json_path=TEST_LAW_JSON,
        terms_json_path=TEST_TERMS_JSON
    )

    # Get some results
    results = rag.retrieve("ceza")

    # Test context formatting
    context = rag.format_context(results)
    assert isinstance(context, str)
    assert len(context) > 0


# Add more tests as needed
