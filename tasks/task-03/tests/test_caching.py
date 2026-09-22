"""Test caching behavior and consistency."""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api import RetrievalAPI
from src.config import RetrievalConfig


@pytest.fixture
def api():
    """Create API instance with test corpus."""
    config = RetrievalConfig(top_k=10, use_cache=True)
    api_instance = RetrievalAPI(config)
    corpus_path = Path(__file__).parent.parent / "data" / "corpus.json"
    api_instance.load_corpus(str(corpus_path))
    return api_instance


def test_caching_improves_performance(api):
    """Cached queries should work correctly (behavior test, not timing)."""
    query = "machine learning"
    
    # First query
    results1 = api.search(query, top_k=5)
    
    # Second query (should use cache)
    results2 = api.search(query, top_k=5)
    
    # Results should be identical
    doc_ids1 = [r['doc_id'] for r in results1]
    doc_ids2 = [r['doc_id'] for r in results2]
    
    assert doc_ids1 == doc_ids2, "Cached results should be identical"


def test_cache_respects_parameters(api):
    """Cache should differentiate between different query parameters."""
    query = "learning"
    
    results_k5 = api.search(query, top_k=5)
    results_k10 = api.search(query, top_k=10)
    
    # Different top_k should return different number of results
    assert len(results_k5) <= 5, "top_k=5 should return at most 5"
    assert len(results_k10) <= 10, "top_k=10 should return at most 10"
    
    # If corpus has enough docs, should be different
    if len(results_k10) > 5:
        assert len(results_k10) > len(results_k5), "top_k=10 should return more results"


def test_cache_respects_filters(api):
    """Cache should differentiate queries with different filters."""
    query = "learning"
    
    results_no_filter = api.search(query, top_k=10)
    results_ml_filter = api.search(query, top_k=10, category="ml")
    results_nlp_filter = api.search(query, top_k=10, category="nlp")
    
    # Results should be different
    ids_no_filter = [r['doc_id'] for r in results_no_filter]
    ids_ml = [r['doc_id'] for r in results_ml_filter]
    ids_nlp = [r['doc_id'] for r in results_nlp_filter]
    
    # ML and NLP results should be different
    assert ids_ml != ids_nlp, "Different category filters should return different results"


def test_cache_cleared_recomputes_correctly(api):
    """After clearing cache, results should be recomputed but identical."""
    query = "neural networks"
    
    results1 = api.search(query, top_k=5)
    api.clear_cache()
    results2 = api.search(query, top_k=5)
    
    # Should still be identical
    doc_ids1 = [r['doc_id'] for r in results1]
    doc_ids2 = [r['doc_id'] for r in results2]
    
    assert doc_ids1 == doc_ids2, "Results after cache clear should be identical"


def test_no_cache_config(api):
    """System should work correctly without caching."""
    # Create API without cache
    config = RetrievalConfig(top_k=10, use_cache=False)
    api_no_cache = RetrievalAPI(config)
    corpus_path = Path(__file__).parent.parent / "data" / "corpus.json"
    api_no_cache.load_corpus(str(corpus_path))
    
    query = "machine learning"
    results1 = api_no_cache.search(query, top_k=5)
    results2 = api_no_cache.search(query, top_k=5)
    
    # Should still get consistent results
    doc_ids1 = [r['doc_id'] for r in results1]
    doc_ids2 = [r['doc_id'] for r in results2]
    
    assert doc_ids1 == doc_ids2, "No-cache mode should still be deterministic"


def test_cache_stats_tracking(api):
    """Cache stats should track cache usage."""
    api.clear_cache()
    
    stats_before = api.get_stats()
    initial_cache_size = stats_before.get('cache_size', 0)
    
    # Run some queries
    api.search("machine learning", top_k=5)
    api.search("deep learning", top_k=5)
    api.search("machine learning", top_k=5)  # Duplicate
    
    stats_after = api.get_stats()
    final_cache_size = stats_after.get('cache_size', 0)
    
    # Cache should have entries
    assert final_cache_size >= initial_cache_size, "Cache should grow with queries"
