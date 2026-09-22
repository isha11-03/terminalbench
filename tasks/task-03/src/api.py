"""External API for retrieval system."""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from .config import RetrievalConfig
from .retrieval import RetrievalEngine, RetrievalResult


class RetrievalAPI:
    """High-level API for document retrieval."""
    
    def __init__(self, config: Optional[RetrievalConfig] = None):
        """
        Initialize retrieval API.
        
        Args:
            config: Configuration object
        """
        self.config = config or RetrievalConfig()
        self.engine = RetrievalEngine(self.config)
    
    def load_corpus(self, corpus_path: str):
        """
        Load document corpus from JSON file.
        
        Args:
            corpus_path: Path to corpus JSON file
        """
        with open(corpus_path, 'r') as f:
            documents = json.load(f)
        
        self.engine.index_documents(documents)
    
    def search(
        self,
        query: str,
        top_k: int = 10,
        category: Optional[str] = None,
        year: Optional[int] = None,
        min_score: float = 0.0,
        rerank: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
            category: Filter by category
            year: Filter by year
            min_score: Minimum similarity score
            rerank: Apply reranking
        
        Returns:
            List of result dictionaries
        """
        # Retrieve documents
        results = self.engine.retrieve(
            query=query,
            top_k=top_k,
            category_filter=category,
            year_filter=year,
            min_score=min_score
        )
        
        # Optional reranking
        if rerank:
            results = self.engine.rerank_results(
                results,
                query=query,
                boost_recent=True
            )
        
        # Convert to dictionaries
        return [
            {
                'doc_id': r.doc_id,
                'score': r.score,
                'rank': r.rank,
                'title': r.metadata.get('title', ''),
                'category': r.metadata.get('category'),
                'year': r.metadata.get('year'),
                'tags': r.metadata.get('tags', [])
            }
            for r in results
        ]
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get document by ID.
        
        Args:
            doc_id: Document ID
        
        Returns:
            Document dictionary or None
        """
        for doc in self.engine.documents:
            if doc['id'] == doc_id:
                return doc
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        return self.engine.get_stats()
    
    def clear_cache(self):
        """Clear all caches."""
        self.engine.clear_cache()
        self.engine.embedding_gen.clear_cache()


def main():
    """Example usage."""
    # Initialize API
    api = RetrievalAPI()
    
    # Load corpus
    corpus_path = Path(__file__).parent.parent / "data" / "corpus.json"
    api.load_corpus(str(corpus_path))
    
    # Example search
    results = api.search("neural networks deep learning", top_k=5)
    
    print(f"Found {len(results)} results:\n")
    for result in results:
        print(f"Rank {result['rank']}: {result['title']}")
        print(f"  Score: {result['score']:.4f}")
        print(f"  Category: {result['category']}, Year: {result['year']}")
        print()


if __name__ == "__main__":
    main()
