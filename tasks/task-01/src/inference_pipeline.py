"""
Baseline ML Inference Pipeline with Multiple Inefficiencies
This implementation has several performance and resource issues that need optimization.
"""
import numpy as np
import pickle
import re
import time
from typing import List, Dict, Any
from pathlib import Path


class TextPreprocessor:
    """Handles text preprocessing with inefficient implementations."""
    
    def __init__(self):
        self.stopwords = self._load_stopwords()
    
    def _load_stopwords(self) -> set:
        """Load stopwords set."""
        # Common English stopwords
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
    
    def preprocess(self, text: str) -> str:
        """Preprocess a single text with inefficient operations."""
        # INEFFICIENCY 1: Multiple unnecessary string copies and passes
        text_copy1 = str(text)
        text_copy2 = text_copy1.lower()
        text_copy3 = text_copy2.strip()
        
        # INEFFICIENCY 2: Character-by-character processing instead of regex
        result = ""
        for char in text_copy3:
            if char.isalnum() or char.isspace():
                result += char
            else:
                result += " "
        
        # INEFFICIENCY 3: Inefficient stopword removal with repeated splits
        words = result.split()
        filtered_words = []
        for word in words:
            if word not in self.stopwords:
                filtered_words.append(word)
        
        # INEFFICIENCY 4: Rebuilding string inefficiently
        final_text = ""
        for i, word in enumerate(filtered_words):
            if i > 0:
                final_text += " "
            final_text += word
        
        return final_text
    
    def preprocess_batch(self, texts: List[str]) -> List[str]:
        """Preprocess a batch of texts."""
        # INEFFICIENCY 5: No batching optimization, processes one by one
        results = []
        for text in texts:
            results.append(self.preprocess(text))
        return results


class FeatureExtractor:
    """Extracts features using TF-IDF vectorization."""
    
    def __init__(self, model_dir: Path):
        self.vectorizer = self._load_vectorizer(model_dir)
        # INEFFICIENCY 6: Cache that's never used effectively
        self._feature_cache = {}
    
    def _load_vectorizer(self, model_dir: Path):
        """Load the TF-IDF vectorizer."""
        vectorizer_path = model_dir / "vectorizer.pkl"
        with open(vectorizer_path, 'rb') as f:
            return pickle.load(f)
    
    def extract_features(self, texts: List[str]) -> np.ndarray:
        """Extract TF-IDF features from texts."""
        # INEFFICIENCY 7: Unnecessary data copying
        texts_copy = [str(t) for t in texts]
        texts_copy2 = list(texts_copy)
        
        # Transform to TF-IDF features
        features = self.vectorizer.transform(texts_copy2)
        
        # INEFFICIENCY 8: Converting to dense unnecessarily for sparse data
        dense_features = features.toarray()
        
        # INEFFICIENCY 9: Another unnecessary copy
        return np.array(dense_features, copy=True)


class ModelInference:
    """Performs model inference."""
    
    def __init__(self, model_dir: Path):
        self.model = self._load_model(model_dir)
        self.label_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
    
    def _load_model(self, model_dir: Path):
        """Load the trained model."""
        model_path = model_dir / "model.pkl"
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    
    def predict(self, features: np.ndarray) -> List[Dict[str, Any]]:
        """Run inference on features."""
        # INEFFICIENCY 10: Repeated probability computation
        predictions = []
        for i in range(len(features)):
            # Extract single sample inefficiently
            sample = features[i:i+1]
            
            # Predict class
            pred_class = self.model.predict(sample)[0]
            
            # INEFFICIENCY 11: Computing probabilities separately
            pred_proba = self.model.predict_proba(sample)[0]
            
            # INEFFICIENCY 12: Redundant probability normalization
            proba_sum = sum(pred_proba)
            normalized_proba = [p / proba_sum for p in pred_proba]
            
            predictions.append({
                'label': self.label_map[pred_class],
                'confidence': float(normalized_proba[pred_class]),
                'probabilities': {
                    self.label_map[j]: float(normalized_proba[j])
                    for j in range(len(normalized_proba))
                }
            })
        
        return predictions


class InferencePipeline:
    """Main inference pipeline - PUBLIC API."""
    
    def __init__(self, model_dir: str = "data/model"):
        """Initialize the inference pipeline.
        
        Args:
            model_dir: Path to the directory containing model artifacts
        """
        self.model_dir = Path(model_dir)
        self.preprocessor = TextPreprocessor()
        self.feature_extractor = FeatureExtractor(self.model_dir)
        self.model_inference = ModelInference(self.model_dir)
        
        # INEFFICIENCY 13: Result cache with poor cache key strategy
        self._result_cache = {}
    
    def predict(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Predict sentiment for a list of texts.
        
        This is the PUBLIC API that must remain compatible.
        
        Args:
            texts: List of input text strings
            
        Returns:
            List of prediction dictionaries with 'label', 'confidence', and 'probabilities'
        """
        if not texts:
            return []
        
        # INEFFICIENCY 14: Cache lookup on entire batch (almost never hits)
        cache_key = str(texts)
        if cache_key in self._result_cache:
            return self._result_cache[cache_key]
        
        # Preprocess
        preprocessed = self.preprocessor.preprocess_batch(texts)
        
        # Extract features
        features = self.feature_extractor.extract_features(preprocessed)
        
        # Run inference
        predictions = self.model_inference.predict(features)
        
        # INEFFICIENCY 15: Storing entire batch results in cache (memory waste)
        self._result_cache[cache_key] = predictions
        
        return predictions
