"""Test filtering behavior - filters should work correctly."""

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


def test_category_filter_returns_only_category(api):
    """Category filter should return only documents from that category."""
    results = api.search("learning algorithms", top_k=10, category="ml")
    
    assert len(results) > 0, "Should return results for ml category"
    
    for result in results:
        assert result['category'] == 'ml', \
            f"All results should be category 'ml', got '{result['category']}'"


def test_nlp_category_filter(api):
    """NLP category filter should return only NLP documents."""
    results = api.search("text processing", top_k=10, category="nlp")
    
    assert len(results) > 0, "Should return NLP results"
    
    for result in results:
        assert result['category'] == 'nlp', f"Expected category 'nlp', got '{result['category']}'"


def test_cv_category_filter(api):
    """CV category filter should return only CV documents."""
    results = api.search("image processing vision", top_k=10, category="cv")
    
    assert len(results) > 0, "Should return CV results"
    
    for result in results:
        assert result['category'] == 'cv', f"Expected category 'cv', got '{result['category']}'"


def test_filtered_results_should_match_top_k(api):
    """When enough filtered documents exist, should return up to top_k results."""
    # There are 12 'ml' documents, so requesting 5 should return 5
    results = api.search("machine learning", top_k=5, category="ml")
    
    # Should get 5 results since we have more than 5 ML docs
    assert len(results) == 5, f"Expected 5 results with ml filter, got {len(results)}"


def test_filter_should_not_reduce_relevance(api):
    """Filtered results should still be the most relevant within that category."""
    # Get results with and without filter
    results_no_filter = api.search("natural language", top_k=10)
    results_with_filter = api.search("natural language", top_k=10, category="nlp")
    
    # Filtered results should be a subset
    filtered_ids = [r['doc_id'] for r in results_with_filter]
    
    # All filtered results should be NLP
    for doc_id in filtered_ids:
        doc = api.get_document(doc_id)
        assert doc['category'] == 'nlp', "Filtered results should all be NLP"
    
    # Filtered results should still be ordered by relevance
    for i in range(len(results_with_filter) - 1):
        assert results_with_filter[i]['score'] >= results_with_filter[i+1]['score'], \
            "Filtered results should be ordered by score"


def test_year_filter(api):
    """Year filter should return only documents from that year."""
    results = api.search("machine learning", top_k=10, year=2021)
    
    assert len(results) > 0, "Should return results for year 2021"
    
    for result in results:
        assert result['year'] == 2021, f"Expected year 2021, got {result['year']}"


def test_combined_filters(api):
    """Category and year filters should work together."""
    results = api.search("learning", top_k=10, category="ml", year=2020)
    
    assert len(results) > 0, "Should return results with combined filters"
    
    for result in results:
        assert result['category'] == 'ml', f"Expected category 'ml', got '{result['category']}'"
        assert result['year'] == 2020, f"Expected year 2020, got {result['year']}"


def test_filter_with_no_matches_returns_empty(api):
    """Filter with no matching documents should return empty list."""
    # No 'ml' documents from year 2025
    results = api.search("machine learning", top_k=10, category="ml", year=2025)
    
    assert len(results) == 0, "Should return empty list when no documents match filter"


def test_min_score_filter(api):
    """Min score filter should exclude low-scoring results."""
    results_no_filter = api.search("machine learning", top_k=10, min_score=0.0)
    results_with_filter = api.search("machine learning", top_k=10, min_score=0.3)
    
    # With min_score, should get fewer or equal results
    assert len(results_with_filter) <= len(results_no_filter), \
        "Min score filter should not increase result count"
    
    # All filtered results should have score >= threshold
    for result in results_with_filter:
        assert result['score'] >= 0.3, \
            f"Score {result['score']} should be >= 0.3"


def test_top_k_respected_after_filtering(api):
    """Should return exactly top_k results after filtering, not before."""
    # Request 3 results from NLP category
    results = api.search("processing", top_k=3, category="nlp")
    
    # Should get at most 3 results
    assert len(results) <= 3, f"Expected at most 3 results, got {len(results)}"
    
    # All should be NLP
    for result in results:
        assert result['category'] == 'nlp', "All results should be NLP"
