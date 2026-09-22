"""
Data preprocessing and normalization.

DEFECT:
- Defect 3: Train/inference preprocessing inconsistency (lines 30-60)
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional


class DataPreprocessor:
    """
    Handles data preprocessing including normalization and missing value handling.
    
    DEFECT 3: Training fits on full dataset (data leakage), and
    inference uses different statistics, creating distribution shift.
    """
    
    def __init__(self):
        self.feature_means_ = None
        self.feature_stds_ = None
        self.fitted_ = False
    
    def fit_transform(self, X: np.ndarray, fit_data: np.ndarray = None) -> np.ndarray:
        """
        Fit preprocessing on data and transform.
        
        DEFECT: fit_data parameter is ignored! Always fits on X,
        causing data leakage when X includes validation/test data.
        
        Args:
            X: Data to transform
            fit_data: Data to fit statistics on (IGNORED - this is the bug!)
            
        Returns:
            Transformed data
        """
        # DEFECT: Should use fit_data if provided, but doesn't!
        # This causes leakage when called with full dataset
        self.feature_means_ = np.mean(X, axis=0)
        self.feature_stds_ = np.std(X, axis=0)
        self.feature_stds_[self.feature_stds_ == 0] = 1.0  # Avoid division by zero
        self.fitted_ = True
        
        # Normalize
        X_normalized = (X - self.feature_means_) / self.feature_stds_
        
        return X_normalized
    
    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform data using fitted statistics.
        
        DEFECT: In inference, if not fitted, uses different normalization!
        """
        if not self.fitted_:
            # DEFECT: Should raise error, but instead computes statistics
            # on the inference data itself, creating distribution shift!
            print("Warning: Preprocessor not fitted, computing statistics on input data")
            self.feature_means_ = np.mean(X, axis=0)
            self.feature_stds_ = np.std(X, axis=0)
            self.feature_stds_[self.feature_stds_ == 0] = 1.0
        
        X_normalized = (X - self.feature_means_) / self.feature_stds_
        
        return X_normalized
    
    def inverse_transform(self, X_normalized: np.ndarray) -> np.ndarray:
        """Inverse transform normalized data."""
        if not self.fitted_:
            raise ValueError("Preprocessor must be fitted before inverse transform")
        
        return X_normalized * self.feature_stds_ + self.feature_means_
    
    def handle_missing_values(self, X: np.ndarray, strategy: str = "mean") -> np.ndarray:
        """
        Handle missing values in features.
        
        DEFECT: Missing value handling is inconsistent - uses different
        strategies in training vs inference implicitly.
        """
        X = X.copy()
        
        if strategy == "mean":
            # Replace NaN with column mean
            col_means = np.nanmean(X, axis=0)
            for i in range(X.shape[1]):
                mask = np.isnan(X[:, i])
                X[mask, i] = col_means[i]
        elif strategy == "zero":
            X[np.isnan(X)] = 0.0
        
        return X
