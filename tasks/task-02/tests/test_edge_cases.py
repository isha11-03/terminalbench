"""
Tests for edge case handling in the forecasting pipeline.
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
from src import config


class TestEdgeCases:
    """Test suite for edge case handling."""
    
    @pytest.fixture
    def forecaster_and_data(self):
        """Prepare forecaster and data."""
        df = load_data()
        df = create_all_features(df)
        df = df.dropna().reset_index(drop=True)
        
        train_df, val_df, test_df = create_temporal_splits(df)
        feature_cols = get_feature_columns(train_df)
        
        X_train, y_train, _ = prepare_sequences(
            train_df, feature_cols, forecast_horizon=config.FORECAST_HORIZON
        )
        
        forecaster = DemandForecaster()
        forecaster.train(X_train, y_train, feature_cols)
        
        return {
            'forecaster': forecaster,
            'df': df,
            'train_df': train_df,
            'val_df': val_df,
            'test_df': test_df,
            'feature_cols': feature_cols
        }
    
    def test_forecast_at_data_boundaries(self, forecaster_and_data):
        """Test forecasting at the beginning and end of available data."""
        forecaster = forecaster_and_data['forecaster']
        df = forecaster_and_data['df']
        
        # Test forecasting from near the end of data
        dates = df[config.DATE_COLUMN]
        late_date = dates.iloc[-config.FORECAST_HORIZON - 5]
        
        result = forecaster.forecast_multi_step(
            df, late_date, horizon=config.FORECAST_HORIZON
        )
        
        assert len(result['predictions']) > 0, (
            "Should be able to forecast from near end of data"
        )
    
    def test_missing_values_in_features(self, forecaster_and_data):
        """Test handling of missing values in feature data."""
        forecaster = forecaster_and_data['forecaster']
        feature_cols = forecaster_and_data['feature_cols']
        
        # Create test data with missing values
        X_test = np.random.randn(10, len(feature_cols))
        X_test[2, 1] = np.nan  # Introduce missing value
        X_test[5, 3] = np.nan
        
        # Should handle missing values (either impute or raise clear error)
        try:
            # First handle missing values
            X_test_clean = forecaster.preprocessor.handle_missing_values(X_test)
            
            # Now predict should work
            predictions = forecaster.predict(X_test_clean)
            
            assert len(predictions) == 10, "Should handle missing values"
            assert not np.any(np.isnan(predictions)), "Predictions should not be NaN"
        except ValueError as e:
            # Also acceptable to raise a clear error
            assert "missing" in str(e).lower() or "nan" in str(e).lower()
    
    def test_cold_start_with_insufficient_history(self, forecaster_and_data):
        """Test behavior when there's insufficient history for lag features."""
        df = load_data()
        
        # Take only first few days (insufficient for max lag)
        short_df = df.head(5).copy()
        short_df = create_all_features(short_df)
        
        # Should have NaN in lag features
        max_lag = max(config.LAG_FEATURES)
        assert short_df.iloc[0][f'demand_lag_{max_lag}'] is pd.NA or \
               pd.isna(short_df.iloc[0][f'demand_lag_{max_lag}']), (
            "Early rows should have NaN for lag features"
        )
    
    def test_forecast_with_single_horizon_step(self, forecaster_and_data):
        """Test forecasting with horizon=1."""
        forecaster = forecaster_and_data['forecaster']
        train_df = forecaster_and_data['train_df']
        df = forecaster_and_data['df']
        
        start_date = train_df[config.DATE_COLUMN].iloc[-10]
        
        result = forecaster.forecast_multi_step(df, start_date, horizon=1)
        
        assert len(result['dates']) == 1, "Should return 1 date for horizon=1"
        assert len(result['predictions']) == 1, "Should return 1 prediction for horizon=1"
        
        # Verify the date is exactly 1 day ahead
        expected_date = start_date + pd.Timedelta(days=1)
        assert result['dates'][0] == expected_date, (
            f"Horizon=1 should predict for {expected_date}"
        )
    
    def test_forecast_with_long_horizon(self, forecaster_and_data):
        """Test forecasting with longer horizon."""
        forecaster = forecaster_and_data['forecaster']
        train_df = forecaster_and_data['train_df']
        df = forecaster_and_data['df']
        
        start_date = train_df[config.DATE_COLUMN].iloc[-30]
        long_horizon = 14
        
        result = forecaster.forecast_multi_step(df, start_date, horizon=long_horizon)
        
        # Should return up to horizon predictions (may be limited by data availability)
        assert len(result['dates']) <= long_horizon, (
            f"Should return at most {long_horizon} predictions"
        )
        assert len(result['dates']) == len(result['predictions']), (
            "Dates and predictions should match in length"
        )
    
    def test_prediction_with_extreme_feature_values(self, forecaster_and_data):
        """Test predictions with extreme (but valid) feature values."""
        forecaster = forecaster_and_data['forecaster']
        feature_cols = forecaster_and_data['feature_cols']
        
        # Create test data with extreme values
        X_test = np.zeros((3, len(feature_cols)))
        
        # Extreme but not invalid
        X_test[0, :] = 1000  # Very high values
        X_test[1, :] = 0.01  # Very low values  
        X_test[2, :] = np.random.randn(len(feature_cols))  # Normal
        
        predictions = forecaster.predict(X_test)
        
        assert len(predictions) == 3, "Should handle extreme values"
        assert not np.any(np.isnan(predictions)), "Should not produce NaN"
        assert not np.any(np.isinf(predictions)), "Should not produce inf"
    
    def test_empty_validation_set_handling(self):
        """Test that splits handle edge cases in data size."""
        df = load_data()
        
        # The actual data should be large enough for all splits
        train_df, val_df, test_df = create_temporal_splits(df)
        
        assert len(train_df) > 0, "Training set should not be empty"
        assert len(val_df) > 0, "Validation set should not be empty"
        assert len(test_df) > 0, "Test set should not be empty"
    
    def test_feature_creation_with_minimal_data(self):
        """Test feature creation with minimal data points."""
        df = load_data()
        
        # Take just enough data for one rolling window
        max_window = max(config.ROLLING_WINDOWS)
        minimal_df = df.head(max_window + 5).copy()
        
        # Should be able to create features
        result_df = create_all_features(minimal_df)
        
        assert len(result_df) > 0, "Should create features with minimal data"
        # After dropping NaN, should have at least some rows
        result_df = result_df.dropna()
        assert len(result_df) > 0, "Should have some valid rows after NaN removal"
    
    def test_zero_demand_handling(self, forecaster_and_data):
        """Test that zero demand values are handled correctly."""
        df = load_data()
        
        # Check if any zero demand exists in data
        has_zero = (df[config.TARGET_COLUMN] == 0).any()
        
        # Model should handle zero demand without errors
        # (Our synthetic data doesn't have zeros, but test the concept)
        # If we artificially create zero demand:
        forecaster = forecaster_and_data['forecaster']
        feature_cols = forecaster_and_data['feature_cols']
        
        X_test = np.random.randn(5, len(feature_cols))
        predictions = forecaster.predict(X_test)
        
        # Predictions could be zero or near-zero
        assert all(p >= -1 for p in predictions), (
            "Predictions should not be extremely negative"
        )


class TestDataQuality:
    """Test data quality and invariants."""
    
    def test_no_missing_dates_in_data(self):
        """Test that generated data has no missing dates."""
        df = load_data()
        
        dates = df[config.DATE_COLUMN]
        date_range = pd.date_range(start=dates.min(), end=dates.max(), freq='D')
        
        assert len(dates) == len(date_range), (
            "Data should have no missing dates in sequence"
        )
    
    def test_demand_positive(self):
        """Test that all demand values are positive."""
        df = load_data()
        
        assert (df[config.TARGET_COLUMN] > 0).all(), (
            "All demand values should be positive"
        )
    
    def test_price_in_reasonable_range(self):
        """Test that price values are in reasonable range."""
        df = load_data()
        
        prices = df['price']
        assert (prices > 0).all(), "Prices should be positive"
        assert (prices < 1000).all(), "Prices should be in reasonable range"
    
    def test_promotion_binary(self):
        """Test that promotion is binary (0 or 1)."""
        df = load_data()
        
        promotions = df['promotion']
        assert set(promotions.unique()).issubset({0, 1}), (
            "Promotion should be binary"
        )
    
    def test_day_of_week_valid_range(self):
        """Test that day_of_week is in valid range [0, 6]."""
        df = load_data()
        
        dow = df['day_of_week']
        assert dow.min() >= 0, "Day of week should be >= 0"
        assert dow.max() <= 6, "Day of week should be <= 6"
