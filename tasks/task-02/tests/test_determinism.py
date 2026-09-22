"""
Tests for determinism and reproducibility.
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


class TestDeterminism:
    """Test suite for determinism and reproducibility."""
    
    def test_data_loading_deterministic(self):
        """Test that data loading is deterministic."""
        df1 = load_data()
        df2 = load_data()
        
        pd.testing.assert_frame_equal(df1, df2, check_exact=True)
    
    def test_feature_creation_deterministic(self):
        """Test that feature creation is deterministic."""
        df = load_data()
        
        features1 = create_all_features(df.copy())
        features2 = create_all_features(df.copy())
        
        pd.testing.assert_frame_equal(
            features1, features2,
            check_exact=False,  # Allow for floating point differences
            rtol=1e-10
        )
    
    def test_temporal_split_deterministic(self):
        """Test that temporal splits are deterministic."""
        df = load_data()
        
        train1, val1, test1 = create_temporal_splits(df)
        train2, val2, test2 = create_temporal_splits(df)
        
        pd.testing.assert_frame_equal(train1, train2)
        pd.testing.assert_frame_equal(val1, val2)
        pd.testing.assert_frame_equal(test1, test2)
    
    def test_model_training_deterministic(self):
        """Test that model training is deterministic with same seed."""
        df = load_data()
        df = create_all_features(df)
        df = df.dropna().reset_index(drop=True)
        
        train_df, _, _ = create_temporal_splits(df)
        feature_cols = get_feature_columns(train_df)
        
        X_train, y_train, _ = prepare_sequences(
            train_df, feature_cols, forecast_horizon=config.FORECAST_HORIZON
        )
        
        # Train two models with same seed
        forecaster1 = DemandForecaster(random_seed=42)
        forecaster1.train(X_train, y_train, feature_cols)
        
        forecaster2 = DemandForecaster(random_seed=42)
        forecaster2.train(X_train, y_train, feature_cols)
        
        # Models should have identical parameters
        np.testing.assert_array_almost_equal(
            forecaster1.model.coef_,
            forecaster2.model.coef_,
            decimal=10,
            err_msg="Model coefficients should be identical with same seed"
        )
        
        np.testing.assert_almost_equal(
            forecaster1.model.intercept_,
            forecaster2.model.intercept_,
            decimal=10,
            err_msg="Model intercept should be identical with same seed"
        )
    
    def test_predictions_deterministic(self):
        """Test that predictions are deterministic."""
        df = load_data()
        df = create_all_features(df)
        df = df.dropna().reset_index(drop=True)
        
        train_df, val_df, _ = create_temporal_splits(df)
        feature_cols = get_feature_columns(train_df)
        
        X_train, y_train, _ = prepare_sequences(
            train_df, feature_cols, forecast_horizon=config.FORECAST_HORIZON
        )
        X_val, _, _ = prepare_sequences(
            val_df, feature_cols, forecast_horizon=config.FORECAST_HORIZON
        )
        
        # Train model
        forecaster = DemandForecaster(random_seed=42)
        forecaster.train(X_train, y_train, feature_cols)
        
        # Make predictions twice
        predictions1 = forecaster.predict(X_val)
        predictions2 = forecaster.predict(X_val)
        
        np.testing.assert_array_almost_equal(
            predictions1,
            predictions2,
            decimal=10,
            err_msg="Predictions should be deterministic"
        )
    
    def test_forecast_deterministic(self):
        """Test that multi-step forecasts are deterministic."""
        df = load_data()
        df = create_all_features(df)
        df = df.dropna().reset_index(drop=True)
        
        train_df, _, _ = create_temporal_splits(df)
        feature_cols = get_feature_columns(train_df)
        
        X_train, y_train, _ = prepare_sequences(
            train_df, feature_cols, forecast_horizon=config.FORECAST_HORIZON
        )
        
        forecaster = DemandForecaster(random_seed=42)
        forecaster.train(X_train, y_train, feature_cols)
        
        start_date = train_df[config.DATE_COLUMN].iloc[-20]
        
        # Generate forecast twice
        forecast1 = forecaster.forecast_multi_step(
            df, start_date, horizon=config.FORECAST_HORIZON
        )
        forecast2 = forecaster.forecast_multi_step(
            df, start_date, horizon=config.FORECAST_HORIZON
        )
        
        # Dates should be identical
        assert forecast1['dates'] == forecast2['dates'], (
            "Forecast dates should be deterministic"
        )
        
        # Predictions should be identical
        np.testing.assert_array_almost_equal(
            forecast1['predictions'],
            forecast2['predictions'],
            decimal=10,
            err_msg="Forecast predictions should be deterministic"
        )
    
    def test_full_pipeline_deterministic(self):
        """Test that the full pipeline run is deterministic."""
        from src.pipeline import run_pipeline
        
        # Run pipeline twice
        results1 = run_pipeline()
        results2 = run_pipeline()
        
        # Compare validation metrics
        assert abs(results1['val_metrics']['mae'] - results2['val_metrics']['mae']) < 1e-10, (
            "Validation MAE should be deterministic"
        )
        assert abs(results1['val_metrics']['rmse'] - results2['val_metrics']['rmse']) < 1e-10, (
            "Validation RMSE should be deterministic"
        )
        
        # Compare test metrics
        assert abs(results1['test_metrics']['mae'] - results2['test_metrics']['mae']) < 1e-10, (
            "Test MAE should be deterministic"
        )
        
        # Compare forecasts
        np.testing.assert_array_almost_equal(
            results1['forecast']['predictions'],
            results2['forecast']['predictions'],
            decimal=10,
            err_msg="Pipeline forecasts should be deterministic"
        )
    
    def test_preprocessing_statistics_deterministic(self):
        """Test that preprocessing statistics are computed deterministically."""
        from src.preprocessing import DataPreprocessor
        
        np.random.seed(42)
        data = np.random.randn(100, 5)
        
        preprocessor1 = DataPreprocessor()
        preprocessor1.fit_transform(data)
        
        preprocessor2 = DataPreprocessor()
        preprocessor2.fit_transform(data)
        
        np.testing.assert_array_almost_equal(
            preprocessor1.feature_means_,
            preprocessor2.feature_means_,
            decimal=10,
            err_msg="Preprocessing means should be deterministic"
        )
        
        np.testing.assert_array_almost_equal(
            preprocessor1.feature_stds_,
            preprocessor2.feature_stds_,
            decimal=10,
            err_msg="Preprocessing stds should be deterministic"
        )


class TestReproducibility:
    """Test reproducibility across different runs."""
    
    def test_same_seed_same_results(self):
        """Test that using the same seed produces identical results."""
        df = load_data()
        df = create_all_features(df)
        df = df.dropna().reset_index(drop=True)
        
        train_df, _, _ = create_temporal_splits(df)
        feature_cols = get_feature_columns(train_df)
        
        X_train, y_train, _ = prepare_sequences(
            train_df, feature_cols, forecast_horizon=config.FORECAST_HORIZON
        )
        
        # Train with seed 42
        forecaster1 = DemandForecaster(random_seed=42)
        forecaster1.train(X_train, y_train, feature_cols)
        pred1 = forecaster1.predict(X_train[:10])
        
        # Train again with seed 42
        forecaster2 = DemandForecaster(random_seed=42)
        forecaster2.train(X_train, y_train, feature_cols)
        pred2 = forecaster2.predict(X_train[:10])
        
        np.testing.assert_array_almost_equal(pred1, pred2, decimal=10)
    
    def test_different_seed_can_differ(self):
        """
        Test that different seeds can produce different results
        (verifies randomness exists but is controlled).
        """
        df = load_data()
        df = create_all_features(df)
        df = df.dropna().reset_index(drop=True)
        
        train_df, _, _ = create_temporal_splits(df)
        feature_cols = get_feature_columns(train_df)
        
        X_train, y_train, _ = prepare_sequences(
            train_df, feature_cols, forecast_horizon=config.FORECAST_HORIZON
        )
        
        # For LinearRegression, results should be the same regardless of seed
        # (no randomness in training). This test verifies that behavior.
        forecaster1 = DemandForecaster(random_seed=42)
        forecaster1.train(X_train, y_train, feature_cols)
        pred1 = forecaster1.predict(X_train[:10])
        
        forecaster2 = DemandForecaster(random_seed=99)
        forecaster2.train(X_train, y_train, feature_cols)
        pred2 = forecaster2.predict(X_train[:10])
        
        # For deterministic models like LinearRegression, should be identical
        np.testing.assert_array_almost_equal(
            pred1, pred2, decimal=10,
            err_msg="LinearRegression should be deterministic regardless of seed"
        )
