"""Test deterministic behavior - same query should always produce same results."""

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


def test_same_query_returns_same_results(api):
    """Running same query multiple times should return identical results."""
    query = "machine learning algorithms"
    
    # Run query multiple times
    results1 = api.search(query, top_k=10)
    results2 = api.search(query, top_k=10)
    results3 = api.search(query, top_k=10)
    
    # Check results are identical
    assert len(results1) == len(results2) == len(results3), "Should return same number of results"
    
    for i in range(len(results1)):
        assert results1[i]['doc_id'] == results2[i]['doc_id'] == results3[i]['doc_id'], \
            f"Doc ID at rank {i+1} should be consistent"
        assert abs(results1[i]['score'] - results2[i]['score']) < 1e-10, \
            f"Score at rank {i+1} should be consistent"


def test_deterministic_ordering_with_ties(api):
    """When scores are equal, ordering should still be deterministic."""
    # Query that might produce ties
    query = "data preprocessing"
    
    results1 = api.search(query, top_k=10)
    results2 = api.search(query, top_k=10)
    
    # Check exact same ordering
    doc_ids1 = [r['doc_id'] for r in results1]
    doc_ids2 = [r['doc_id'] for r in results2]
    
    assert doc_ids1 == doc_ids2, "Document ordering should be deterministic even with potential ties"


def test_multiple_queries_deterministic(api):
    """Multiple different queries should all be deterministic."""
    queries = [
        "neural networks",
        "natural language processing",
        "computer vision",
        "optimization algorithms",
        "embeddings vectors"
    ]
    
    for query in queries:
        results1 = api.search(query, top_k=5)
        results2 = api.search(query, top_k=5)
        
        doc_ids1 = [r['doc_id'] for r in results1]
        doc_ids2 = [r['doc_id'] for r in results2]
        
        assert doc_ids1 == doc_ids2, f"Query '{query}' should be deterministic"


def test_cache_cleared_same_results(api):
    """Clearing cache should not affect results."""
    query = "deep learning"
    
    results1 = api.search(query, top_k=5)
    api.clear_cache()
    results2 = api.search(query, top_k=5)
    
    doc_ids1 = [r['doc_id'] for r in results1]
    doc_ids2 = [r['doc_id'] for r in results2]
    
    assert doc_ids1 == doc_ids2, "Results should be same after cache clear"


def test_deterministic_across_api_instances(api):
    """Same query on different API instances should return same results."""
    query = "machine learning"
    
    # First instance results
    results1 = api.search(query, top_k=5)
    
    # Create new instance
    config = RetrievalConfig(top_k=10)
    api2 = RetrievalAPI(config)
    corpus_path = Path(__file__).parent.parent / "data" / "corpus.json"
    api2.load_corpus(str(corpus_path))
    
    # Second instance results
    results2 = api2.search(query, top_k=5)
    
    # Compare
    doc_ids1 = [r['doc_id'] for r in results1]
    doc_ids2 = [r['doc_id'] for r in results2]
    
    assert doc_ids1 == doc_ids2, "Different API instances should return same results"


def test_scores_consistent_across_runs(api):
    """Similarity scores should be exactly the same across runs."""
    query = "neural networks"
    
    results1 = api.search(query, top_k=5)
    results2 = api.search(query, top_k=5)
    
    for i in range(len(results1)):
        score_diff = abs(results1[i]['score'] - results2[i]['score'])
        assert score_diff < 1e-10, f"Scores should be identical, got diff {score_diff}"
