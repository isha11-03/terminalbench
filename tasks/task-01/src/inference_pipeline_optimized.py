"""
Optimized ML Inference Pipeline
This is the oracle solution with all inefficiencies fixed.
"""
import numpy as np
import pickle
import re
from typing import List, Dict, Any
from pathlib import Path


class TextPreprocessor:
    """Handles text preprocessing with optimized implementations."""
    
    def __init__(self):
        self.stopwords = self._load_stopwords()
        # Compile regex once for efficiency
        self._nonalnum_pattern = re.compile(r'[^a-z0-9\s]+')
        self._whitespace_pattern = re.compile(r'\s+')
    
    def _load_stopwords(self) -> set:
        """Load stopwords set."""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
    
    def preprocess(self, text: str) -> str:
        """Preprocess a single text with optimized operations."""
        # FIX 1: Single pass lowercase and strip
        text = text.lower().strip()
        
        # FIX 2: Use regex for efficient character cleaning
        text = self._nonalnum_pattern.sub(' ', text)
        
        # FIX 3: Normalize whitespace
        text = self._whitespace_pattern.sub(' ', text)
        
        # FIX 4: Efficient stopword removal using list comprehension and join
        words = text.split()
        filtered_words = [w for w in words if w not in self.stopwords]
        
        return ' '.join(filtered_words)
    
    def preprocess_batch(self, texts: List[str]) -> List[str]:
        """Preprocess a batch of texts."""
        # FIX 5: List comprehension is already efficient, no change needed
        return [self.preprocess(text) for text in texts]


class FeatureExtractor:
    """Extracts features using TF-IDF vectorization."""
    
    def __init__(self, model_dir: Path):
        self.vectorizer = self._load_vectorizer(model_dir)
    
    def _load_vectorizer(self, model_dir: Path):
        """Load the TF-IDF vectorizer."""
        vectorizer_path = model_dir / "vectorizer.pkl"
        with open(vectorizer_path, 'rb') as f:
            return pickle.load(f)
    
    def extract_features(self, texts: List[str]) -> np.ndarray:
        """Extract TF-IDF features from texts."""
        # FIX 7: Remove unnecessary data copying
        # FIX 8: Keep sparse matrix format (don't convert to dense)
        features = self.vectorizer.transform(texts)
        
        # FIX 9: Return sparse matrix directly, avoid unnecessary copy
        return features


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
        # FIX 10-11: Batch predict and predict_proba once
        pred_classes = self.model.predict(features)
        pred_probas = self.model.predict_proba(features)
        
        predictions = []
        for i in range(len(pred_classes)):
            pred_class = pred_classes[i]
            pred_proba = pred_probas[i]
            
            # FIX 12: No need to normalize, predict_proba already returns normalized probabilities
            predictions.append({
                'label': self.label_map[pred_class],
                'confidence': float(pred_proba[pred_class]),
                'probabilities': {
                    self.label_map[j]: float(pred_proba[j])
                    for j in range(len(pred_proba))
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
        
        # FIX 13-15: Remove ineffective caching (cache hit rate was near zero)
        # Caching entire batches is inefficient and wastes memory
        
        # Preprocess
        preprocessed = self.preprocessor.preprocess_batch(texts)
        
        # Extract features
        features = self.feature_extractor.extract_features(preprocessed)
        
        # Run inference
        predictions = self.model_inference.predict(features)
        
        return predictions
