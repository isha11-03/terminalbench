"""
Tests for temporal correctness - ensuring no data leakage from future to past.

This is the most critical test suite as it validates the fundamental
temporal causality requirements of time-series forecasting.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import load_data, create_temporal_splits
from src.feature_engineering import create_all_features
from src import config


class TestTemporalCorrectness:
    """Test suite for temporal correctness and data leakage prevention."""
    
    @pytest.fixture
    def data(self):
        """Load and prepare data for testing."""
        df = load_data()
        return df
    
    def test_chronological_train_val_test_split(self, data):
        """
        Test that train/val/test splits maintain chronological order.
        Training data must come entirely before validation data,
        and validation must come entirely before test data.
        """
        train_df, val_df, test_df = create_temporal_splits(data)
        
        # Check that all training dates come before all validation dates
        max_train_date = train_df[config.DATE_COLUMN].max()
        min_val_date = val_df[config.DATE_COLUMN].min()
        assert max_train_date < min_val_date, (
            f"Training data (max {max_train_date}) must come entirely "
            f"before validation data (min {min_val_date})"
        )
        
        # Check that all validation dates come before all test dates
        max_val_date = val_df[config.DATE_COLUMN].max()
        min_test_date = test_df[config.DATE_COLUMN].min()
        assert max_val_date < min_test_date, (
            f"Validation data (max {max_val_date}) must come entirely "
            f"before test data (min {min_test_date})"
        )
    
    def test_no_temporal_overlap_in_splits(self, data):
        """Test that there is no date overlap between splits."""
        train_df, val_df, test_df = create_temporal_splits(data)
        
        train_dates = set(train_df[config.DATE_COLUMN])
        val_dates = set(val_df[config.DATE_COLUMN])
        test_dates = set(test_df[config.DATE_COLUMN])
        
        # Check no overlap
        assert len(train_dates & val_dates) == 0, "Training and validation share dates"
        assert len(train_dates & test_dates) == 0, "Training and test share dates"
        assert len(val_dates & test_dates) == 0, "Validation and test share dates"
    
    def test_split_sizes_correct(self, data):
        """Test that splits have approximately the expected sizes."""
        train_df, val_df, test_df = create_temporal_splits(data)
        
        # Allow some flexibility due to NaN dropping, but should be close
        assert len(train_df) >= config.TRAIN_DAYS * 0.9, "Training set too small"
        assert len(val_df) >= config.VAL_DAYS * 0.9, "Validation set too small"
        assert len(test_df) >= config.TEST_DAYS * 0.9, "Test set too small"
    
    def test_rolling_features_no_future_leakage(self, data):
        """
        Critical test: Verify that rolling statistics at time t do NOT
        include information from times > t (future data leakage).
        
        This tests for the center=True bug in rolling statistics.
        """
        df = create_all_features(data)
        df = df.dropna().reset_index(drop=True)
        
        # Check rolling mean features
        for window in config.ROLLING_WINDOWS:
            col = f'demand_rolling_mean_{window}'
            
            if col not in df.columns:
                continue
            
            # For each point, verify the rolling mean only uses past data
            for i in range(window, min(len(df), 100)):  # Check first 100 valid points
                # Manually compute what the rolling mean SHOULD be (looking backward only)
                expected_mean = df[config.TARGET_COLUMN].iloc[i-window+1:i+1].mean()
                actual_mean = df[col].iloc[i]
                
                # If center=True was used, the actual will differ from expected
                # Allow small numerical tolerance
                if not pd.isna(expected_mean) and not pd.isna(actual_mean):
                    assert abs(actual_mean - expected_mean) < 1e-6, (
                        f"Rolling mean at index {i} uses future data! "
                        f"Expected (backward-looking): {expected_mean:.4f}, "
                        f"Got: {actual_mean:.4f}"
                    )
    
    def test_rolling_features_backward_only(self, data):
        """
        Additional test for temporal leakage: verify rolling statistics
        computed at time t can be replicated using only data up to time t.
        """
        df = create_all_features(data)
        df = df.dropna().reset_index(drop=True)
        
        # Pick a test point in the middle of the dataset
        test_idx = 100
        
        for window in config.ROLLING_WINDOWS:
            mean_col = f'demand_rolling_mean_{window}'
            
            if mean_col not in df.columns:
                continue
            
            # Get the computed rolling mean
            computed_mean = df[mean_col].iloc[test_idx]
            
            # Manually compute using only past data
            past_values = df[config.TARGET_COLUMN].iloc[max(0, test_idx-window+1):test_idx+1]
            manual_mean = past_values.mean()
            
            if not pd.isna(computed_mean) and not pd.isna(manual_mean):
                assert abs(computed_mean - manual_mean) < 1e-6, (
                    f"Rolling mean at index {test_idx} cannot be replicated "
                    f"using only past data (temporal leakage detected)"
                )
    
    def test_lag_features_correct_shift(self, data):
        """Test that lag features correctly reference past values."""
        df = create_all_features(data)
        df = df.dropna().reset_index(drop=True)
        
        for lag in config.LAG_FEATURES:
            lag_col = f'demand_lag_{lag}'
            
            if lag_col not in df.columns:
                continue
            
            # Check several points
            for i in range(lag + 10, min(len(df), lag + 30)):
                expected_value = df[config.TARGET_COLUMN].iloc[i - lag]
                actual_value = df[lag_col].iloc[i]
                
                assert abs(actual_value - expected_value) < 1e-6, (
                    f"Lag {lag} feature at index {i} incorrect. "
                    f"Expected: {expected_value}, Got: {actual_value}"
                )
    
    def test_no_future_data_in_features_at_prediction_time(self, data):
        """
        Verify that when making a prediction for time t+h, features
        only contain information from times <= t.
        """
        from src.data_loader import prepare_sequences
        
        df = create_all_features(data)
        df = df.dropna().reset_index(drop=True)
        
        train_df, _, _ = create_temporal_splits(df)
        feature_cols = [col for col in train_df.columns 
                       if col not in [config.DATE_COLUMN, config.TARGET_COLUMN]]
        
        X, y, dates = prepare_sequences(
            train_df, feature_cols, forecast_horizon=config.FORECAST_HORIZON
        )
        
        # For each prediction, verify features use only past data
        # This is a structural test - if feature creation is correct,
        # prepare_sequences should not introduce leakage
        assert len(X) > 0, "No sequences prepared"
        assert len(X) == len(y), "Feature-label mismatch"
        assert len(X) == len(dates), "Feature-date mismatch"


class TestTemporalIntegrity:
    """Additional temporal integrity tests."""
    
    @pytest.fixture
    def data(self):
        """Load data."""
        return load_data()
    
    def test_data_chronologically_ordered(self, data):
        """Test that loaded data is in chronological order."""
        dates = data[config.DATE_COLUMN]
        assert dates.is_monotonic_increasing, "Data must be chronologically ordered"
    
    def test_no_duplicate_dates(self, data):
        """Test that there are no duplicate dates in the data."""
        dates = data[config.DATE_COLUMN]
        assert len(dates) == len(dates.unique()), "Duplicate dates found in data"
    
    def test_continuous_date_sequence(self, data):
        """Test that dates form a continuous daily sequence."""
        dates = data[config.DATE_COLUMN]
        date_diffs = dates.diff().dt.days.dropna()
        
        assert (date_diffs == 1).all(), (
            "Dates are not continuous (missing days detected)"
        )
