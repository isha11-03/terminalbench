"""
Tests for forecast horizon correctness - ensuring predictions align with correct future dates.
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


class TestForecastHorizon:
    """Test suite for forecast horizon accuracy and date alignment."""
    
    @pytest.fixture
    def prepared_data(self):
        """Prepare data and model for testing."""
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
            'df': df,
            'train_df': train_df,
            'forecaster': forecaster,
            'feature_cols': feature_cols
        }
    
    def test_forecast_returns_correct_number_of_steps(self, prepared_data):
        """Test that forecast returns exactly the requested horizon length."""
        forecaster = prepared_data['forecaster']
        train_df = prepared_data['train_df']
        df = prepared_data['df']
        
        start_date = train_df[config.DATE_COLUMN].iloc[-30]
        horizon = config.FORECAST_HORIZON
        
        result = forecaster.forecast_multi_step(df, start_date, horizon=horizon)
        
        assert 'dates' in result, "Forecast must include 'dates'"
        assert 'predictions' in result, "Forecast must include 'predictions'"
        assert len(result['dates']) == horizon, (
            f"Forecast should return {horizon} dates, got {len(result['dates'])}"
        )
        assert len(result['predictions']) == horizon, (
            f"Forecast should return {horizon} predictions, got {len(result['predictions'])}"
        )
    
    def test_forecast_dates_are_future_from_start(self, prepared_data):
        """Test that all forecast dates are in the future relative to start date."""
        forecaster = prepared_data['forecaster']
        train_df = prepared_data['train_df']
        df = prepared_data['df']
        
        start_date = train_df[config.DATE_COLUMN].iloc[-30]
        
        result = forecaster.forecast_multi_step(
            df, start_date, horizon=config.FORECAST_HORIZON
        )
        
        for i, forecast_date in enumerate(result['dates']):
            assert forecast_date > start_date, (
                f"Forecast date {i} ({forecast_date}) must be after "
                f"start date ({start_date})"
            )
    
    def test_forecast_dates_correct_offset(self, prepared_data):
        """
        Critical test: Verify forecast dates are exactly 1, 2, ..., horizon days
        ahead of the start date.
        """
        forecaster = prepared_data['forecaster']
        train_df = prepared_data['train_df']
        df = prepared_data['df']
        
        start_date = train_df[config.DATE_COLUMN].iloc[-30]
        horizon = config.FORECAST_HORIZON
        
        result = forecaster.forecast_multi_step(df, start_date, horizon=horizon)
        
        for i, forecast_date in enumerate(result['dates']):
            expected_date = start_date + pd.Timedelta(days=i+1)
            
            assert forecast_date == expected_date, (
                f"Forecast step {i+1} should be for date {expected_date}, "
                f"but got {forecast_date}"
            )
    
    def test_forecast_dates_consecutive(self, prepared_data):
        """Test that forecast dates are consecutive days."""
        forecaster = prepared_data['forecaster']
        train_df = prepared_data['train_df']
        df = prepared_data['df']
        
        start_date = train_df[config.DATE_COLUMN].iloc[-30]
        
        result = forecaster.forecast_multi_step(
            df, start_date, horizon=config.FORECAST_HORIZON
        )
        
        dates = result['dates']
        for i in range(1, len(dates)):
            date_diff = (dates[i] - dates[i-1]).days
            assert date_diff == 1, (
                f"Forecast dates should be consecutive. Gap of {date_diff} days "
                f"between {dates[i-1]} and {dates[i]}"
            )
    
    def test_prepare_sequences_target_alignment(self, prepared_data):
        """
        Test that prepare_sequences correctly aligns features with targets
        that are 'forecast_horizon' steps ahead.
        """
        train_df = prepared_data['train_df']
        feature_cols = prepared_data['feature_cols']
        horizon = config.FORECAST_HORIZON
        
        X, y, dates = prepare_sequences(
            train_df, feature_cols, forecast_horizon=horizon
        )
        
        # For each sequence, verify the target is exactly 'horizon' days ahead
        for i in range(min(10, len(X))):  # Check first 10 samples
            # Get the date for this prediction
            pred_date = dates[i]
            
            # Find the feature row in the original dataframe
            # The features should be from (pred_date - horizon days)
            expected_feature_date = pred_date - pd.Timedelta(days=horizon)
            
            # Verify this date exists and alignment is correct
            feature_rows = train_df[train_df[config.DATE_COLUMN] == expected_feature_date]
            
            if len(feature_rows) > 0:
                # Verify target matches the demand at prediction date
                target_rows = train_df[train_df[config.DATE_COLUMN] == pred_date]
                if len(target_rows) > 0:
                    expected_target = target_rows.iloc[0][config.TARGET_COLUMN]
                    actual_target = y[i]
                    
                    assert abs(actual_target - expected_target) < 1e-6, (
                        f"Target at index {i} misaligned. "
                        f"Expected {expected_target}, got {actual_target}"
                    )
    
    def test_multi_step_forecast_consistency(self, prepared_data):
        """
        Test that running forecast multiple times from same point gives
        consistent dates.
        """
        forecaster = prepared_data['forecaster']
        train_df = prepared_data['train_df']
        df = prepared_data['df']
        
        start_date = train_df[config.DATE_COLUMN].iloc[-30]
        
        result1 = forecaster.forecast_multi_step(
            df, start_date, horizon=config.FORECAST_HORIZON
        )
        result2 = forecaster.forecast_multi_step(
            df, start_date, horizon=config.FORECAST_HORIZON
        )
        
        # Dates should be identical
        assert result1['dates'] == result2['dates'], (
            "Forecast dates should be deterministic"
        )
        
        # Predictions should be identical (determinism test)
        np.testing.assert_array_almost_equal(
            result1['predictions'],
            result2['predictions'],
            decimal=6,
            err_msg="Forecast predictions should be deterministic"
        )
    
    def test_forecast_different_horizons(self, prepared_data):
        """Test forecasting with different horizon lengths."""
        forecaster = prepared_data['forecaster']
        train_df = prepared_data['train_df']
        df = prepared_data['df']
        
        start_date = train_df[config.DATE_COLUMN].iloc[-30]
        
        for horizon in [3, 5, 7, 14]:
            result = forecaster.forecast_multi_step(df, start_date, horizon=horizon)
            
            assert len(result['dates']) == horizon, (
                f"Horizon {horizon}: expected {horizon} dates, "
                f"got {len(result['dates'])}"
            )
            assert len(result['predictions']) == horizon, (
                f"Horizon {horizon}: expected {horizon} predictions, "
                f"got {len(result['predictions'])}"
            )
            
            # Verify first and last dates
            first_expected = start_date + pd.Timedelta(days=1)
            last_expected = start_date + pd.Timedelta(days=horizon)
            
            assert result['dates'][0] == first_expected, (
                f"Horizon {horizon}: first date should be {first_expected}"
            )
            assert result['dates'][-1] == last_expected, (
                f"Horizon {horizon}: last date should be {last_expected}"
            )


class TestForecastOutput:
    """Test forecast output format and validity."""
    
    @pytest.fixture
    def forecaster_and_data(self):
        """Prepare forecaster and data."""
        df = load_data()
        df = create_all_features(df)
        df = df.dropna().reset_index(drop=True)
        
        train_df, _, _ = create_temporal_splits(df)
        feature_cols = get_feature_columns(train_df)
        
        X_train, y_train, _ = prepare_sequences(
            train_df, feature_cols, forecast_horizon=config.FORECAST_HORIZON
        )
        
        forecaster = DemandForecaster()
        forecaster.train(X_train, y_train, feature_cols)
        
        return forecaster, df, train_df
    
    def test_forecast_predictions_are_numeric(self, forecaster_and_data):
        """Test that all predictions are valid numbers."""
        forecaster, df, train_df = forecaster_and_data
        
        start_date = train_df[config.DATE_COLUMN].iloc[-10]
        result = forecaster.forecast_multi_step(
            df, start_date, horizon=config.FORECAST_HORIZON
        )
        
        for i, pred in enumerate(result['predictions']):
            assert isinstance(pred, (int, float, np.number)), (
                f"Prediction {i} is not numeric: {type(pred)}"
            )
            assert not np.isnan(pred), f"Prediction {i} is NaN"
            assert not np.isinf(pred), f"Prediction {i} is infinite"
    
    def test_forecast_predictions_reasonable_range(self, forecaster_and_data):
        """Test that predictions are in a reasonable range (not negative, not extreme)."""
        forecaster, df, train_df = forecaster_and_data
        
        start_date = train_df[config.DATE_COLUMN].iloc[-10]
        result = forecaster.forecast_multi_step(
            df, start_date, horizon=config.FORECAST_HORIZON
        )
        
        # Demand should be positive
        for i, pred in enumerate(result['predictions']):
            assert pred >= 0, f"Prediction {i} is negative: {pred}"
            
            # Should be within reasonable bounds (not more than 10x the max demand)
            max_demand = df[config.TARGET_COLUMN].max()
            assert pred <= 10 * max_demand, (
                f"Prediction {i} is unreasonably high: {pred}"
            )
