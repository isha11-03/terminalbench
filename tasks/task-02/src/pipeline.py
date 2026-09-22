"""
Main forecasting pipeline orchestration.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from . import config
from .data_loader import load_data, create_temporal_splits, prepare_sequences
from .feature_engineering import create_all_features, get_feature_columns
from .forecaster import DemandForecaster


def run_pipeline(
    data_path: str = None,
    forecast_horizon: int = config.FORECAST_HORIZON
) -> Dict:
    """
    Run the complete forecasting pipeline.
    
    This orchestrates all components, each of which may have defects.
    
    Returns:
        Dictionary containing model, metrics, and forecasts
    """
    # Load data
    print("Loading data...")
    df = load_data(data_path)
    
    # Create features (DEFECT 1: temporal leakage in rolling features)
    print("Creating features...")
    df = create_all_features(df)
    
    # Drop rows with NaN (from lag features at the beginning)
    df = df.dropna().reset_index(drop=True)
    
    # Split data (DEFECT 4: random shuffle instead of chronological)
    print("Splitting data...")
    train_df, val_df, test_df = create_temporal_splits(df)
    
    # Get feature columns
    feature_cols = get_feature_columns(train_df)
    
    # Prepare sequences (DEFECT 5: feature-label misalignment)
    print("Preparing sequences...")
    X_train, y_train, _ = prepare_sequences(
        train_df, feature_cols, forecast_horizon=forecast_horizon
    )
    X_val, y_val, val_dates = prepare_sequences(
        val_df, feature_cols, forecast_horizon=forecast_horizon
    )
    X_test, y_test, test_dates = prepare_sequences(
        test_df, feature_cols, forecast_horizon=forecast_horizon
    )
    
    # Train model (DEFECT 3: preprocessing inconsistency)
    print("Training model...")
    forecaster = DemandForecaster()
    forecaster.train(X_train, y_train, feature_cols)
    
    # Evaluate on validation set
    print("Evaluating on validation set...")
    val_metrics = forecaster.evaluate(X_val, y_val)
    print(f"Validation MAE: {val_metrics['mae']:.2f}")
    print(f"Validation RMSE: {val_metrics['rmse']:.2f}")
    print(f"Validation MAPE: {val_metrics['mape']:.2f}%")
    
    # Evaluate on test set
    print("Evaluating on test set...")
    test_metrics = forecaster.evaluate(X_test, y_test)
    print(f"Test MAE: {test_metrics['mae']:.2f}")
    print(f"Test RMSE: {test_metrics['rmse']:.2f}")
    print(f"Test MAPE: {test_metrics['mape']:.2f}%")
    
    # Generate forecast (DEFECT 2: incorrect horizon handling)
    print(f"Generating {forecast_horizon}-day forecast...")
    
    # Use the last date in training data as start point
    last_train_date = train_df[config.DATE_COLUMN].iloc[-1]
    
    # Forecast from this point (bugs in forecast_multi_step will manifest here)
    forecast_result = forecaster.forecast_multi_step(
        df, last_train_date, horizon=forecast_horizon
    )
    
    return {
        'model': forecaster,
        'val_metrics': val_metrics,
        'test_metrics': test_metrics,
        'forecast': forecast_result,
        'train_df': train_df,
        'val_df': val_df,
        'test_df': test_df,
        'feature_cols': feature_cols
    }


if __name__ == "__main__":
    # Run the pipeline
    results = run_pipeline()
    
    print("\n=== Pipeline Complete ===")
    print(f"Forecast dates: {results['forecast']['dates']}")
    print(f"Forecast values: {results['forecast']['predictions']}")
