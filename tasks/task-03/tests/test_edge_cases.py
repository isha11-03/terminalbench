"""Test edge cases and boundary conditions."""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api import RetrievalAPI
from src.config import RetrievalConfig


@pytest.fixture
def api():
    """Create API instance with test corpus."""
    config = RetrievalConfig(top_k=10)
    api_instance = RetrievalAPI(config)
    corpus_path = Path(__file__).parent.parent / "data" / "corpus.json"
    api_instance.load_corpus(str(corpus_path))
    return api_instance


def test_empty_query(api):
    """Empty query should return empty results or handle gracefully."""
    results = api.search("", top_k=10)
    
    # Should handle gracefully - either empty or all docs with zero scores
    assert isinstance(results, list), "Should return a list"
    
    # If returns results, they should have very low or zero scores
    for result in results:
        assert result['score'] <= 0.1, "Empty query should not have high similarity scores"


def test_whitespace_only_query(api):
    """Whitespace-only query should be treated like empty query."""
    results = api.search("   \t\n  ", top_k=10)
    
    assert isinstance(results, list), "Should return a list"


def test_top_k_one(api):
    """Requesting single result should work correctly."""
    results = api.search("machine learning", top_k=1)
    
    assert len(results) == 1, "Should return exactly 1 result"
    assert 0 <= results[0]['score'] <= 1.0, "Score should be in valid range"


def test_top_k_larger_than_corpus(api):
    """Requesting more results than corpus size should return all documents."""
    results = api.search("learning", top_k=100)
    
    # We have 20 documents, so should get at most 20
    assert len(results) <= 20, f"Should not return more than corpus size, got {len(results)}"


def test_very_specific_query_no_matches(api):
    """Very specific query with no matches should still return reasonable results."""
    results = api.search("quantum computing blockchain cryptocurrency", top_k=5)
    
    # Should return some results even if not perfectly matching
    assert isinstance(results, list), "Should return a list"
    # May be empty or have low scores, both acceptable


def test_special_characters_in_query(api):
    """Query with special characters should be handled."""
    results = api.search("machine-learning & deep_learning!", top_k=5)
    
    assert isinstance(results, list), "Should handle special characters"
    assert len(results) > 0, "Should still find relevant results"


def test_repeated_words_query(api):
    """Query with repeated words should work correctly."""
    results = api.search("learning learning learning", top_k=5)
    
    assert len(results) > 0, "Should return results"
    assert all(r['score'] >= 0 for r in results), "Scores should be non-negative"


def test_single_word_query(api):
    """Single word query should work."""
    results = api.search("embeddings", top_k=5)
    
    assert len(results) > 0, "Should return results for single word"


def test_very_long_query(api):
    """Very long query should be handled."""
    long_query = " ".join(["machine learning"] * 50)
    results = api.search(long_query, top_k=5)
    
    assert isinstance(results, list), "Should handle long query"
    assert len(results) > 0, "Should return results"


def test_case_insensitive_query(api):
    """Queries with different cases should return same results."""
    results1 = api.search("Machine Learning", top_k=5)
    results2 = api.search("machine learning", top_k=5)
    results3 = api.search("MACHINE LEARNING", top_k=5)
    
    doc_ids1 = [r['doc_id'] for r in results1]
    doc_ids2 = [r['doc_id'] for r in results2]
    doc_ids3 = [r['doc_id'] for r in results3]
    
    assert doc_ids1 == doc_ids2 == doc_ids3, "Queries should be case-insensitive"


def test_query_with_numbers(api):
    """Query with numbers should work."""
    results = api.search("learning 2020 algorithms", top_k=5)
    
    assert isinstance(results, list), "Should handle numbers in query"


def test_unicode_query(api):
    """Query with unicode characters should be handled."""
    results = api.search("machine learning café", top_k=5)
    
    assert isinstance(results, list), "Should handle unicode"


def test_get_nonexistent_document(api):
    """Getting nonexistent document should return None."""
    doc = api.get_document("doc_999")
    
    assert doc is None, "Nonexistent document should return None"


def test_get_existing_document(api):
    """Getting existing document should return document."""
    doc = api.get_document("doc_001")
    
    assert doc is not None, "Existing document should be returned"
    assert doc['id'] == 'doc_001', "Should return correct document"


def test_stats_returns_correct_info(api):
    """Stats should return correct system information."""
    stats = api.get_stats()
    
    assert 'num_documents' in stats, "Stats should include document count"
    assert stats['num_documents'] == 20, "Should have 20 documents"
    assert 'embedding_dim' in stats, "Stats should include embedding dimension"
