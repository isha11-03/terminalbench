"""Document retrieval and ranking engine."""

import numpy as np
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from .embeddings import EmbeddingGenerator, batch_cosine_similarity
from .preprocessing import preprocess_text
from .config import RetrievalConfig


@dataclass
class RetrievalResult:
    """Result from retrieval."""
    doc_id: str
    score: float
    rank: int
    metadata: Dict[str, Any]


class RetrievalEngine:
    """Document retrieval and ranking engine."""
    
    def __init__(self, config: Optional[RetrievalConfig] = None):
        """
        Initialize retrieval engine.
        
        Args:
            config: Configuration object
        """
        self.config = config or RetrievalConfig()
        self.embedding_gen = EmbeddingGenerator(
            dim=self.config.embedding_dim,
            seed=42
        )
        
        # Document storage
        self.documents = []
        self.doc_embeddings = None
        self.doc_metadata = {}
        
        # Query cache
        self._query_cache = {}
        self._config_hash = None
    
    def index_documents(self, documents: List[Dict[str, Any]]):
        """
        Index documents for retrieval.
        
        Args:
            documents: List of document dicts with 'id', 'text', and optional metadata
        """
        self.documents = documents
        self.doc_metadata = {}
        
        # Extract embeddings
        embeddings = []
        for doc in documents:
            doc_id = doc['id']
            
            # Get or generate embedding
            if 'embedding' in doc:
                emb = np.array(doc['embedding'])
            else:
                # Combine title and text
                text = doc.get('title', '') + ' ' + doc.get('text', '')
                text = preprocess_text(
                    text,
                    lowercase=self.config.lowercase,
                    remove_punctuation=self.config.remove_punctuation
                )
                emb = self.embedding_gen.generate(text, normalize=True)
            
            embeddings.append(emb)
            
            # Store metadata
            self.doc_metadata[doc_id] = {
                'category': doc.get('category'),
                'year': doc.get('year'),
                'tags': doc.get('tags', []),
                'title': doc.get('title', ''),
                'text': doc.get('text', '')
            }
        
        self.doc_embeddings = np.array(embeddings)
        print(f"Indexed {len(documents)} documents")
        
        # Update config hash
        self._update_config_hash()
    
    def _update_config_hash(self):
        """Update hash of current configuration."""
        config_str = f"{self.config.lowercase}_{self.config.remove_punctuation}"
        self._config_hash = hash(config_str)
    
    def _get_current_config_hash(self) -> int:
        """Get current configuration hash."""
        config_str = f"{self.config.lowercase}_{self.config.remove_punctuation}"
        return hash(config_str)
    
    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        category_filter: Optional[str] = None,
        year_filter: Optional[int] = None,
        min_score: Optional[float] = None
    ) -> List[RetrievalResult]:
        """
        Retrieve relevant documents for query.
        
        Args:
            query: Query text
            top_k: Number of results to return
            category_filter: Filter by category
            year_filter: Filter by year
            min_score: Minimum similarity score
        
        Returns:
            List of retrieval results
        """
        if self.doc_embeddings is None or len(self.documents) == 0:
            return []
        
        top_k = top_k or self.config.top_k
        min_score = min_score or self.config.similarity_threshold
        
        # FIX 5: Check if config changed and invalidate cache
        current_config_hash = self._get_current_config_hash()
        if self._config_hash != current_config_hash:
            self._query_cache.clear()
            self._config_hash = current_config_hash
        
        # Check cache
        cache_key = (query, top_k, category_filter, year_filter, min_score)
        if self.config.use_cache and cache_key in self._query_cache:
            return self._query_cache[cache_key]
        
        # Preprocess query
        processed_query = preprocess_text(
            query,
            lowercase=self.config.lowercase,
            remove_punctuation=self.config.remove_punctuation
        )
        
        # FIX 1 & 2: Query embedding should be normalized (consistent with corpus)
        query_embedding = self.embedding_gen.generate(processed_query, normalize=True)
        
        # Compute similarities
        similarities = batch_cosine_similarity(query_embedding, self.doc_embeddings)
        
        # FIX 3: Apply filters BEFORE taking top-k
        # Build list of (index, score, doc) tuples for filtering
        candidates = []
        for idx in range(len(self.documents)):
            doc = self.documents[idx]
            doc_id = doc['id']
            score = float(similarities[idx])
            metadata = self.doc_metadata[doc_id]
            
            # Apply filters
            if category_filter and metadata.get('category') != category_filter:
                continue
            if year_filter and metadata.get('year') != year_filter:
                continue
            if score < min_score:
                continue
            
            candidates.append((idx, score, doc_id, metadata))
        
        # FIX 4: Sort with secondary key for deterministic tie handling
        # Sort by score (descending) and then by doc_id (ascending) for determinism
        candidates.sort(key=lambda x: (-x[1], x[2]))
        
        # Take top-k AFTER filtering
        candidates = candidates[:top_k]
        
        # Build results
        results = []
        for rank, (idx, score, doc_id, metadata) in enumerate(candidates, start=1):
            results.append(RetrievalResult(
                doc_id=doc_id,
                score=score,
                rank=rank,
                metadata=metadata
            ))
        
        # Cache result
        if self.config.use_cache:
            self._query_cache[cache_key] = results
        
        return results
    
    def rerank_results(
        self,
        results: List[RetrievalResult],
        query: str,
        boost_recent: bool = False
    ) -> List[RetrievalResult]:
        """
        Rerank results with additional signals.
        
        Args:
            results: Initial retrieval results
            query: Original query
            boost_recent: Boost recent documents
        
        Returns:
            Reranked results
        """
        if not results:
            return results
        
        # Apply boosting
        reranked = []
        for result in results:
            adjusted_score = result.score
            
            if boost_recent and 'year' in result.metadata:
                year = result.metadata['year']
                # Boost recent documents
                year_boost = (year - 2015) * 0.01  # Simple recency boost
                adjusted_score += year_boost
            
            reranked.append((adjusted_score, result.doc_id, result))
        
        # FIX 4: Sort with secondary key for deterministic ordering
        reranked.sort(key=lambda x: (-x[0], x[1]))
        
        # Update ranks and scores
        final_results = []
        for rank, (score, doc_id, result) in enumerate(reranked, start=1):
            result.score = score
            result.rank = rank
            final_results.append(result)
        
        return final_results
    
    def clear_cache(self):
        """Clear query cache."""
        self._query_cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get retrieval engine statistics."""
        return {
            'num_documents': len(self.documents),
            'embedding_dim': self.config.embedding_dim,
            'cache_size': len(self._query_cache),
            'categories': len(set(meta.get('category') for meta in self.doc_metadata.values() if meta.get('category')))
        }
