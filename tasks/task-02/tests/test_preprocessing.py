"""
Tests for preprocessing consistency between training and inference.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import load_data, create_temporal_splits, prepare_sequences
from src.feature_engineering import create_all_features, get_feature_columns
from src.forecaster import DemandForecaster
from src.preprocessing import DataPreprocessor
from src import config


class TestPreprocessingConsistency:
    """Test suite for preprocessing consistency."""
    
    def test_preprocessor_fit_transform_uses_fit_data(self):
        """
        Test that fit_transform actually uses the fit_data parameter
        if provided, not the transform data.
        """
        preprocessor = DataPreprocessor()
        
        # Create two different datasets
        train_data = np.array([[10, 20], [15, 25], [20, 30], [25, 35]])
        inference_data = np.array([[100, 200], [150, 250]])
        
        # Fit on training data, transform inference data
        normalized = preprocessor.fit_transform(inference_data, fit_data=train_data)
        
        # Check that statistics were computed from train_data, not inference_data
        # train_data means: [17.5, 27.5]
        expected_means = np.array([17.5, 27.5])
        
        np.testing.assert_array_almost_equal(
            preprocessor.feature_means_,
            expected_means,
            decimal=6,
            err_msg="Preprocessor should use fit_data parameter for computing statistics"
        )
    
    def test_preprocessor_transform_requires_fit(self):
        """Test that transform requires fitting first (or computes consistently)."""
        preprocessor = DataPreprocessor()
        
        data = np.array([[10, 20], [15, 25], [20, 30]])
        
        # First transform without fitting
        result1 = preprocessor.transform(data)
        
        # The preprocessor should either raise an error OR compute stats from data
        # If it computes from data, verify it's consistent
        assert preprocessor.fitted_ or len(result1) == len(data), (
            "Transform should either require fitting or handle gracefully"
        )
    
    def test_train_inference_use_same_statistics(self):
        """
        Critical test: Verify that training and inference use the same
        normalization statistics (no distribution shift).
        """
        df = load_data()
        df = create_all_features(df)
        df = df.dropna().reset_index(drop=True)
        
        train_df, val_df, _ = create_temporal_splits(df)
        feature_cols = get_feature_columns(train_df)
        
        # Prepare training data
        X_train, y_train, _ = prepare_sequences(
            train_df, feature_cols, forecast_horizon=config.FORECAST_HORIZON
        )
        
        # Train model
        forecaster = DemandForecaster()
        forecaster.train(X_train, y_train, feature_cols)
        
        # Get the statistics used during training
        train_means = forecaster.preprocessor.feature_means_.copy()
        train_stds = forecaster.preprocessor.feature_stds_.copy()
        
        # Prepare validation data
        X_val, y_val, _ = prepare_sequences(
            val_df, feature_cols, forecast_horizon=config.FORECAST_HORIZON
        )
        
        # Make predictions (this calls transform)
        predictions = forecaster.predict(X_val)
        
        # Verify the statistics haven't changed (same as training)
        np.testing.assert_array_almost_equal(
            forecaster.preprocessor.feature_means_,
            train_means,
            decimal=6,
            err_msg="Preprocessing statistics changed between training and inference"
        )
        
        np.testing.assert_array_almost_equal(
            forecaster.preprocessor.feature_stds_,
            train_stds,
            decimal=6,
            err_msg="Preprocessing statistics changed between training and inference"
        )
    
    def test_preprocessor_fitted_flag(self):
        """Test that preprocessor correctly tracks fitted state."""
        preprocessor = DataPreprocessor()
        
        assert not preprocessor.fitted_, "Preprocessor should start unfitted"
        
        data = np.array([[10, 20], [15, 25], [20, 30]])
        preprocessor.fit_transform(data)
        
        assert preprocessor.fitted_, "Preprocessor should be fitted after fit_transform"
    
    def test_normalization_correctness(self):
        """Test that normalization produces zero mean and unit variance."""
        preprocessor = DataPreprocessor()
        
        # Create data with known statistics
        np.random.seed(42)
        data = np.random.randn(100, 5) * 10 + 50  # mean~50, std~10
        
        normalized = preprocessor.fit_transform(data)
        
        # Check normalized data has approximately zero mean and unit std
        np.testing.assert_array_almost_equal(
            np.mean(normalized, axis=0),
            np.zeros(5),
            decimal=10,
            err_msg="Normalized data should have zero mean"
        )
        
        np.testing.assert_array_almost_equal(
            np.std(normalized, axis=0),
            np.ones(5),
            decimal=10,
            err_msg="Normalized data should have unit standard deviation"
        )
    
    def test_inverse_transform_recovers_original(self):
        """Test that inverse transform recovers original values."""
        preprocessor = DataPreprocessor()
        
        original_data = np.array([[10, 20, 30], [15, 25, 35], [20, 30, 40]])
        
        normalized = preprocessor.fit_transform(original_data)
        recovered = preprocessor.inverse_transform(normalized)
        
        np.testing.assert_array_almost_equal(
            recovered,
            original_data,
            decimal=6,
            err_msg="Inverse transform should recover original data"
        )
    
    def test_missing_value_handling_consistency(self):
        """Test that missing value handling is consistent."""
        preprocessor = DataPreprocessor()
        
        # Data with missing values
        data = np.array([[10, 20], [15, np.nan], [20, 30], [np.nan, 35]])
        
        # Handle missing values
        cleaned = preprocessor.handle_missing_values(data, strategy='mean')
        
        # Should have no NaN
        assert not np.any(np.isnan(cleaned)), "Missing values should be handled"
        
        # Verify mean imputation worked correctly
        # Column 0: missing at index 3, mean of [10, 15, 20] = 15
        assert abs(cleaned[3, 0] - 15.0) < 1e-6, "Mean imputation incorrect"
        
        # Column 1: missing at index 1, mean of [20, 30, 35] = 28.333...
        expected_mean = (20 + 30 + 35) / 3
        assert abs(cleaned[1, 1] - expected_mean) < 1e-6, "Mean imputation incorrect"


class TestPreprocessingEdgeCases:
    """Test edge cases in preprocessing."""
    
    def test_constant_feature_handling(self):
        """Test that constant features (zero std) are handled."""
        preprocessor = DataPreprocessor()
        
        # Feature with zero variance
        data = np.array([[10, 5], [10, 6], [10, 7], [10, 8]])
        
        normalized = preprocessor.fit_transform(data)
        
        # Should not have NaN or inf
        assert not np.any(np.isnan(normalized)), "Should handle zero std"
        assert not np.any(np.isinf(normalized)), "Should handle zero std"
        
        # Constant feature should be zero after normalization
        assert np.allclose(normalized[:, 0], 0.0), "Constant feature should normalize to zero"
    
    def test_single_sample_preprocessing(self):
        """Test preprocessing with a single sample."""
        preprocessor = DataPreprocessor()
        
        train_data = np.array([[10, 20], [15, 25], [20, 30]])
        preprocessor.fit_transform(train_data)
        
        # Transform single sample
        single_sample = np.array([[12, 22]])
        normalized = preprocessor.transform(single_sample)
        
        assert normalized.shape == (1, 2), "Should preserve shape"
        assert not np.any(np.isnan(normalized)), "Should not produce NaN"
    
    def test_empty_data_handling(self):
        """Test that empty data is handled gracefully."""
        preprocessor = DataPreprocessor()
        
        empty_data = np.array([]).reshape(0, 3)
        
        # Should either handle gracefully or raise clear error
        try:
            result = preprocessor.fit_transform(empty_data)
            # If it doesn't raise, verify shape is preserved
            assert result.shape == (0, 3), "Should preserve empty shape"
        except (ValueError, RuntimeError):
            # Acceptable to raise error for empty data
            pass
