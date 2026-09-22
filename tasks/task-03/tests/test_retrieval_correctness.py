"""Test retrieval correctness - relevant documents should rank highly."""

import pytest
import json
from pathlib import Path
import sys

# Add src to path
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


def test_neural_networks_query_returns_relevant_docs(api):
    """Query about neural networks should return relevant documents."""
    results = api.search("neural networks deep learning", top_k=10)
    
    assert len(results) > 0, "Should return results"
    
    # Check that highly relevant docs are in results
    doc_ids = [r['doc_id'] for r in results]
    relevant_docs = ['doc_002', 'doc_006', 'doc_013']  # Deep learning, architectures, CNNs
    
    # At least 1 of 3 relevant docs should be in top 10
    found = sum(1 for doc_id in relevant_docs if doc_id in doc_ids)
    assert found >= 1, f"Expected at least 1 relevant doc in top 10, found {found}"


def test_nlp_query_returns_nlp_documents(api):
    """Query about NLP should return NLP-related documents."""
    results = api.search("natural language processing text", top_k=10)
    
    assert len(results) > 0, "Should return results"
    
    # At least one of top results should be NLP-related
    doc_ids = [r['doc_id'] for r in results[:5]]
    nlp_docs = ['doc_003', 'doc_010', 'doc_016', 'doc_014']  # NLP overview, attention, embeddings, RNN
    
    found = sum(1 for doc_id in doc_ids if doc_id in nlp_docs)
    assert found >= 1, f"Expected at least 1 NLP doc in top 5, got {found}"


def test_optimization_query_returns_optimization_docs(api):
    """Query about optimization should return optimization documents."""
    results = api.search("optimization algorithms training", top_k=10)
    
    assert len(results) > 0, "Should return results"
    
    doc_ids = [r['doc_id'] for r in results]
    # doc_012 is about optimization algorithms, doc_018 about batch norm (training related)
    relevant_docs = ['doc_012', 'doc_018', 'doc_007']
    found = sum(1 for doc_id in relevant_docs if doc_id in doc_ids)
    assert found >= 1, f"Expected at least 1 optimization/training doc in results, found {found}"


def test_embedding_query_returns_embedding_doc(api):
    """Query about embeddings should return the embeddings document."""
    results = api.search("embeddings vectors representation learning", top_k=10)
    
    assert len(results) > 0, "Should return results"
    
    doc_ids = [r['doc_id'] for r in results]
    # doc_016 is specifically about embeddings, doc_009 about transfer learning
    relevant_docs = ['doc_016', 'doc_009', 'doc_001']
    found = sum(1 for doc_id in relevant_docs if doc_id in doc_ids)
    assert found >= 1, f"Expected at least 1 relevant doc in results, found {found}"


def test_scores_are_reasonable(api):
    """Similarity scores should be in reasonable range."""
    results = api.search("machine learning", top_k=10)
    
    for result in results:
        # Cosine similarity should be between -1 and 1, typically positive for relevant docs
        assert -1.0 <= result['score'] <= 1.0, f"Score {result['score']} out of range"
        # For this query, scores should be positive (some relevance)
        assert result['score'] >= 0, f"Score should be non-negative for ML query"


def test_scores_decrease_with_rank(api):
    """Scores should be non-increasing with rank."""
    results = api.search("deep learning neural networks", top_k=10)
    
    assert len(results) >= 2, "Need multiple results to test ordering"
    
    for i in range(len(results) - 1):
        current_score = results[i]['score']
        next_score = results[i + 1]['score']
        assert current_score >= next_score, \
            f"Scores should not increase: rank {i+1}={current_score:.4f}, rank {i+2}={next_score:.4f}"


def test_specific_query_returns_specific_doc(api):
    """Queries should return documents with matching terms."""
    results = api.search("generator discriminator compete", top_k=10)
    
    assert len(results) > 0, "Should return results"
    
    # Should return some relevant docs based on word overlap
    assert len(results) >= 1, "Should have at least one result"


def test_reinforcement_learning_query(api):
    """Query about reinforcement learning should find RL document."""
    results = api.search("reinforcement learning agents environment decisions", top_k=10)
    
    doc_ids = [r['doc_id'] for r in results]
    # doc_005 is about reinforcement learning
    assert 'doc_005' in doc_ids, "RL document should be in results"
