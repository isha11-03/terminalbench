"""Configuration for retrieval system."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class RetrievalConfig:
    """Configuration for retrieval pipeline."""
    
    # Embedding parameters
    embedding_dim: int = 64
    normalize_embeddings: bool = True
    
    # Retrieval parameters
    top_k: int = 10
    similarity_threshold: float = 0.0
    
    # Preprocessing
    lowercase: bool = True
    remove_punctuation: bool = False
    
    # Caching
    use_cache: bool = True
    
    # Ranking
    rerank: bool = False
    
    def __post_init__(self):
        """Validate configuration."""
        if self.top_k < 1:
            raise ValueError("top_k must be >= 1")
        if self.embedding_dim < 1:
            raise ValueError("embedding_dim must be >= 1")
