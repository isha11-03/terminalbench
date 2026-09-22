"""
Integration tests for the complete forecasting pipeline.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import run_pipeline
from src import config


class TestPipelineIntegration:
    """Integration tests for the complete pipeline."""
    
    def test_full_pipeline_runs(self):
        """Test that the full pipeline runs without errors."""
        results = run_pipeline()
        
        assert 'model' in results, "Pipeline should return model"
        assert 'val_metrics' in results, "Pipeline should return validation metrics"
        assert 'test_metrics' in results, "Pipeline should return test metrics"
        assert 'forecast' in results, "Pipeline should return forecast"
    
    def test_validation_metrics_reasonable(self):
        """Test that validation metrics are in reasonable ranges."""
        results = run_pipeline()
        
        val_metrics = results['val_metrics']
        
        assert 'mae' in val_metrics, "Should include MAE"
        assert 'rmse' in val_metrics, "Should include RMSE"
        assert 'mape' in val_metrics, "Should include MAPE"
        
        # Metrics should be positive
        assert val_metrics['mae'] > 0, "MAE should be positive"
        assert val_metrics['rmse'] > 0, "RMSE should be positive"
        assert val_metrics['mape'] > 0, "MAPE should be positive"
        
        # RMSE should be >= MAE
        assert val_metrics['rmse'] >= val_metrics['mae'], "RMSE should be >= MAE"
        
        # MAPE should be in reasonable range (percentage)
        assert val_metrics['mape'] < 1000, "MAPE should be in reasonable range"
    
    def test_test_metrics_reasonable(self):
        """Test that test metrics are in reasonable ranges."""
        results = run_pipeline()
        
        test_metrics = results['test_metrics']
        
        assert test_metrics['mae'] > 0, "Test MAE should be positive"
        assert test_metrics['rmse'] > 0, "Test RMSE should be positive"
        assert test_metrics['mape'] > 0, "Test MAPE should be positive"
        
        # RMSE should be >= MAE
        assert test_metrics['rmse'] >= test_metrics['mae'], "RMSE should be >= MAE"
    
    def test_forecast_structure(self):
        """Test that forecast has correct structure."""
        results = run_pipeline()
        
        forecast = results['forecast']
        
        assert 'dates' in forecast, "Forecast should include dates"
        assert 'predictions' in forecast, "Forecast should include predictions"
        
        assert len(forecast['dates']) == len(forecast['predictions']), (
            "Dates and predictions should have same length"
        )
        
        # Should have forecasted for the specified horizon
        assert len(forecast['dates']) <= config.FORECAST_HORIZON, (
            f"Forecast should have at most {config.FORECAST_HORIZON} steps"
        )
    
    def test_forecast_predictions_valid(self):
        """Test that forecast predictions are valid numbers."""
        results = run_pipeline()
        
        predictions = results['forecast']['predictions']
        
        for pred in predictions:
            assert isinstance(pred, (int, float, np.number)), "Prediction should be numeric"
            assert not np.isnan(pred), "Prediction should not be NaN"
            assert not np.isinf(pred), "Prediction should not be infinite"
            assert pred >= 0, "Demand prediction should be non-negative"
    
    def test_trained_model_can_predict(self):
        """Test that trained model can make predictions."""
        results = run_pipeline()
        
        model = results['model']
        train_df = results['train_df']
        feature_cols = results['feature_cols']
        
        # Create a test sample
        sample_features = train_df[feature_cols].iloc[0].values.reshape(1, -1)
        
        # Should be able to predict
        prediction = model.predict(sample_features)
        
        assert len(prediction) == 1, "Should return one prediction"
        assert not np.isnan(prediction[0]), "Prediction should not be NaN"
    
    def test_data_splits_complete(self):
        """Test that data splits cover all data."""
        results = run_pipeline()
        
        train_df = results['train_df']
        val_df = results['val_df']
        test_df = results['test_df']
        
        # All splits should have data
        assert len(train_df) > 0, "Training set should not be empty"
        assert len(val_df) > 0, "Validation set should not be empty"
        assert len(test_df) > 0, "Test set should not be empty"
        
        # Total should be reasonable (accounting for dropped NaN rows)
        total_samples = len(train_df) + len(val_df) + len(test_df)
        expected_total = config.TRAIN_DAYS + config.VAL_DAYS + config.TEST_DAYS
        
        # Allow some flexibility for NaN dropping
        assert total_samples >= expected_total * 0.8, (
            f"Total samples ({total_samples}) seems too low compared to expected ({expected_total})"
        )
    
    def test_feature_columns_reasonable(self):
        """Test that feature columns are reasonable."""
        results = run_pipeline()
        
        feature_cols = results['feature_cols']
        
        assert len(feature_cols) > 0, "Should have at least one feature"
        
        # Should include lag features
        lag_features = [f'demand_lag_{lag}' for lag in config.LAG_FEATURES]
        for lag_feat in lag_features:
            assert lag_feat in feature_cols, f"Should include {lag_feat}"
        
        # Should include some rolling features
        rolling_prefixes = ['demand_rolling_mean_', 'demand_rolling_std_']
        has_rolling = any(
            any(col.startswith(prefix) for prefix in rolling_prefixes)
            for col in feature_cols
        )
        assert has_rolling, "Should include rolling features"
    
    def test_pipeline_reproducible(self):
        """Test that running pipeline twice gives same results."""
        results1 = run_pipeline()
        results2 = run_pipeline()
        
        # Metrics should be identical
        np.testing.assert_almost_equal(
            results1['val_metrics']['mae'],
            results2['val_metrics']['mae'],
            decimal=6,
            err_msg="Pipeline should be reproducible"
        )
        
        # Forecasts should be identical
        np.testing.assert_array_almost_equal(
            results1['forecast']['predictions'],
            results2['forecast']['predictions'],
            decimal=6,
            err_msg="Forecasts should be reproducible"
        )


class TestEndToEnd:
    """End-to-end workflow tests."""
    
    def test_data_generation_and_loading(self):
        """Test that data can be generated and loaded."""
        from src.data_loader import load_data
        
        df = load_data()
        
        assert len(df) > 0, "Should load data"
        assert config.DATE_COLUMN in df.columns, "Should have date column"
        assert config.TARGET_COLUMN in df.columns, "Should have target column"
    
    def test_feature_engineering_workflow(self):
        """Test feature engineering workflow."""
        from src.data_loader import load_data
        from src.feature_engineering import create_all_features, get_feature_columns
        
        df = load_data()
        df_with_features = create_all_features(df)
        feature_cols = get_feature_columns(df_with_features)
        
        assert len(feature_cols) > len(df.columns) - 2, (
            "Should create additional features"
        )
    
    def test_train_predict_workflow(self):
        """Test basic train and predict workflow."""
        from src.data_loader import load_data, create_temporal_splits, prepare_sequences
        from src.feature_engineering import create_all_features, get_feature_columns
        from src.forecaster import DemandForecaster
        
        # Load and prepare data
        df = load_data()
        df = create_all_features(df)
        df = df.dropna().reset_index(drop=True)
        
        train_df, val_df, _ = create_temporal_splits(df)
        feature_cols = get_feature_columns(train_df)
        
        X_train, y_train, _ = prepare_sequences(train_df, feature_cols)
        X_val, y_val, _ = prepare_sequences(val_df, feature_cols)
        
        # Train
        forecaster = DemandForecaster()
        forecaster.train(X_train, y_train, feature_cols)
        
        # Predict
        predictions = forecaster.predict(X_val)
        
        assert len(predictions) == len(y_val), "Should predict for all validation samples"
        assert not np.any(np.isnan(predictions)), "Predictions should not be NaN"
    
    def test_evaluation_workflow(self):
        """Test evaluation workflow."""
        from src.data_loader import load_data, create_temporal_splits, prepare_sequences
        from src.feature_engineering import create_all_features, get_feature_columns
        from src.forecaster import DemandForecaster
        
        df = load_data()
        df = create_all_features(df)
        df = df.dropna().reset_index(drop=True)
        
        train_df, val_df, _ = create_temporal_splits(df)
        feature_cols = get_feature_columns(train_df)
        
        X_train, y_train, _ = prepare_sequences(train_df, feature_cols)
        X_val, y_val, _ = prepare_sequences(val_df, feature_cols)
        
        forecaster = DemandForecaster()
        forecaster.train(X_train, y_train, feature_cols)
        
        metrics = forecaster.evaluate(X_val, y_val)
        
        assert 'mae' in metrics, "Should compute MAE"
        assert 'rmse' in metrics, "Should compute RMSE"
        assert 'mape' in metrics, "Should compute MAPE"
