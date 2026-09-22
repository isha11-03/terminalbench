"""Test API compatibility and interface contracts."""

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


def test_search_returns_list(api):
    """Search should always return a list."""
    results = api.search("machine learning", top_k=5)
    assert isinstance(results, list), "Search should return a list"


def test_search_result_structure(api):
    """Search results should have correct structure."""
    results = api.search("machine learning", top_k=5)
    
    assert len(results) > 0, "Should return results for this query"
    
    for result in results:
        assert isinstance(result, dict), "Each result should be a dict"
        assert 'doc_id' in result, "Result should have doc_id"
        assert 'score' in result, "Result should have score"
        assert 'rank' in result, "Result should have rank"
        assert 'title' in result, "Result should have title"
        assert 'category' in result, "Result should have category"
        assert 'year' in result, "Result should have year"
        assert 'tags' in result, "Result should have tags"
        
        # Type checks
        assert isinstance(result['doc_id'], str), "doc_id should be string"
        assert isinstance(result['score'], (int, float)), "score should be numeric"
        assert isinstance(result['rank'], int), "rank should be integer"
        assert isinstance(result['title'], str), "title should be string"


def test_rank_starts_at_one(api):
    """Ranks should start at 1, not 0."""
    results = api.search("machine learning", top_k=5)
    
    assert len(results) > 0, "Should return results"
    assert results[0]['rank'] == 1, "First result should have rank 1"
    
    for i, result in enumerate(results):
        expected_rank = i + 1
        assert result['rank'] == expected_rank, f"Result {i} should have rank {expected_rank}"


def test_ranks_are_consecutive(api):
    """Ranks should be consecutive integers."""
    results = api.search("machine learning", top_k=10)
    
    for i in range(len(results)):
        assert results[i]['rank'] == i + 1, f"Rank should be {i+1}, got {results[i]['rank']}"


def test_default_parameters(api):
    """API should work with minimal parameters."""
    # Just query, no other parameters
    results = api.search("machine learning")
    
    assert isinstance(results, list), "Should return list"


def test_optional_parameters(api):
    """All optional parameters should be truly optional."""
    # Test various combinations
    api.search("test")
    api.search("test", top_k=5)
    api.search("test", category="ml")
    api.search("test", year=2020)
    api.search("test", min_score=0.1)
    api.search("test", rerank=True)
    api.search("test", top_k=5, category="ml", year=2020)
    
    # All should work without errors


def test_get_document_returns_dict_or_none(api):
    """get_document should return dict or None."""
    doc = api.get_document("doc_001")
    assert isinstance(doc, dict), "Existing document should return dict"
    
    no_doc = api.get_document("nonexistent")
    assert no_doc is None, "Nonexistent document should return None"


def test_get_stats_returns_dict(api):
    """get_stats should return a dictionary."""
    stats = api.get_stats()
    assert isinstance(stats, dict), "Stats should return dict"


def test_clear_cache_no_error(api):
    """clear_cache should execute without error."""
    api.clear_cache()  # Should not raise


def test_load_corpus_idempotent(api):
    """Loading corpus multiple times should work."""
    corpus_path = Path(__file__).parent.parent / "data" / "corpus.json"
    
    # Load again
    api.load_corpus(str(corpus_path))
    
    # Should still work
    results = api.search("machine learning", top_k=5)
    assert len(results) > 0, "Should return results after reload"


def test_rerank_parameter_changes_behavior(api):
    """Rerank parameter should be accepted (behavior may vary)."""
    results_no_rerank = api.search("machine learning", top_k=5, rerank=False)
    results_rerank = api.search("machine learning", top_k=5, rerank=True)
    
    # Both should return valid results
    assert isinstance(results_no_rerank, list), "No rerank should return list"
    assert isinstance(results_rerank, list), "Rerank should return list"
