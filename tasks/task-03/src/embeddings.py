"""Embedding generation and utilities."""

import numpy as np
import hashlib
from typing import Optional


class EmbeddingGenerator:
    """Generate deterministic embeddings from text."""
    
    def __init__(self, dim: int = 64, seed: int = 42):
        """
        Initialize embedding generator.
        
        Args:
            dim: Embedding dimensionality
            seed: Random seed for determinism
        """
        self.dim = dim
        self.seed = seed
        self._cache = {}
    
    def generate(self, text: str, normalize: bool = True) -> np.ndarray:
        """
        Generate embedding for text.
        
        Args:
            text: Input text
            normalize: Whether to normalize to unit vector
        
        Returns:
            Embedding vector
        """
        if not text or not text.strip():
            return np.zeros(self.dim)
        
        # Check cache
        cache_key = (text, normalize)
        if cache_key in self._cache:
            return self._cache[cache_key].copy()
        
        # Normalize text
        text = text.lower().strip()
        words = text.split()
        
        if not words:
            return np.zeros(self.dim)
        
        # Count words for TF-like weighting
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # Generate embedding from unique words with their frequencies
        embedding = np.zeros(self.dim)
        for word, count in word_count.items():
            word_seed = self.seed + self._hash_word(word)
            rng = np.random.RandomState(word_seed)
            word_vec = rng.randn(self.dim)
            # Weight by word frequency (sublinear scaling)
            weight = np.sqrt(count)
            embedding += word_vec * weight
        
        # Length normalization
        doc_length_norm = 1.0 / np.sqrt(len(words))
        embedding = embedding * doc_length_norm
        
        # Normalize
        if normalize:
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
        
        # Cache result
        self._cache[cache_key] = embedding.copy()
        
        return embedding
    
    def _hash_word(self, word: str) -> int:
        """Generate deterministic hash for word."""
        return int(hashlib.md5(word.encode()).hexdigest(), 16) % (2**31)
    
    def clear_cache(self):
        """Clear embedding cache."""
        self._cache.clear()
    
    def batch_generate(self, texts: list[str], normalize: bool = True) -> np.ndarray:
        """
        Generate embeddings for batch of texts.
        
        Args:
            texts: List of input texts
            normalize: Whether to normalize embeddings
        
        Returns:
            Array of embeddings (n_texts, dim)
        """
        embeddings = []
        for text in texts:
            emb = self.generate(text, normalize=normalize)
            embeddings.append(emb)
        return np.array(embeddings)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    
    Args:
        a: First vector
        b: Second vector
    
    Returns:
        Cosine similarity in [-1, 1]
    """
    if len(a.shape) == 1 and len(b.shape) == 1:
        # Single vector case
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))
    else:
        raise ValueError("Expected 1D vectors")


def batch_cosine_similarity(query_embedding: np.ndarray, corpus_embeddings: np.ndarray) -> np.ndarray:
    """
    Compute cosine similarity between query and corpus embeddings.
    
    Args:
        query_embedding: Query vector (dim,)
        corpus_embeddings: Corpus vectors (n_docs, dim)
    
    Returns:
        Similarity scores (n_docs,)
    """
    # Normalize query
    query_norm = np.linalg.norm(query_embedding)
    if query_norm == 0:
        return np.zeros(len(corpus_embeddings))
    
    query_normalized = query_embedding / query_norm
    
    # Normalize corpus (assume already normalized but check)
    corpus_norms = np.linalg.norm(corpus_embeddings, axis=1, keepdims=True)
    corpus_norms = np.where(corpus_norms == 0, 1, corpus_norms)
    corpus_normalized = corpus_embeddings / corpus_norms
    
    # Compute dot product
    similarities = np.dot(corpus_normalized, query_normalized)
    
    return similarities
