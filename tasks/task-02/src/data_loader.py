"""
Data loading and temporal splitting.

DEFECTS:
- Defect 4: Uses random shuffle instead of chronological split (line 45-50)
- Defect 5: Feature-label misalignment by 1 timestep (line 85-90)
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict
from . import config


def load_data(data_path: str = None) -> pd.DataFrame:
    """Load demand data from CSV."""
    if data_path is None:
        data_path = config.DATA_PATH
    
    df = pd.read_csv(data_path)
    df[config.DATE_COLUMN] = pd.to_datetime(df[config.DATE_COLUMN])
    df = df.sort_values(config.DATE_COLUMN).reset_index(drop=True)
    
    return df


def create_temporal_splits(
    df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split data into train, validation, and test sets.
    
    DEFECT 4: This implementation uses RANDOM SHUFFLE instead of proper
    chronological splitting, violating temporal causality.
    
    Args:
        df: Full dataset
        
    Returns:
        train_df, val_df, test_df
    """
    total_days = len(df)
    
    # DEFECT: Random shuffle breaks temporal ordering!
    # This allows future data to appear in training set
    np.random.seed(config.RANDOM_SEED)
    shuffled_indices = np.random.permutation(total_days)
    df_shuffled = df.iloc[shuffled_indices].reset_index(drop=True)
    
    # Split using the shuffled data
    train_end = config.TRAIN_DAYS
    val_end = train_end + config.VAL_DAYS
    
    train_df = df_shuffled.iloc[:train_end].copy()
    val_df = df_shuffled.iloc[train_end:val_end].copy()
    test_df = df_shuffled.iloc[val_end:].copy()
    
    # Re-sort each split by date (but damage is done - validation contains past data)
    train_df = train_df.sort_values(config.DATE_COLUMN).reset_index(drop=True)
    val_df = val_df.sort_values(config.DATE_COLUMN).reset_index(drop=True)
    test_df = test_df.sort_values(config.DATE_COLUMN).reset_index(drop=True)
    
    return train_df, val_df, test_df


def prepare_sequences(
    df: pd.DataFrame,
    feature_cols: list,
    target_col: str = config.TARGET_COLUMN,
    forecast_horizon: int = config.FORECAST_HORIZON
) -> Tuple[np.ndarray, np.ndarray, pd.DatetimeIndex]:
    """
    Prepare feature sequences and targets for forecasting.
    
    DEFECT 5: Feature-label MISALIGNMENT - features and targets are
    off by one timestep due to incorrect indexing.
    
    Args:
        df: DataFrame with features and target
        feature_cols: List of feature column names
        target_col: Target column name
        forecast_horizon: Number of steps ahead to forecast
        
    Returns:
        X (features), y (targets), dates (corresponding dates)
    """
    X_list = []
    y_list = []
    date_list = []
    
    # Need enough history for features and room for forecast horizon
    for i in range(len(df) - forecast_horizon):
        # DEFECT: This takes features at time i
        features = df.iloc[i][feature_cols].values
        
        # DEFECT: But takes target at time i + forecast_horizon - 1
        # Should be i + forecast_horizon, creating off-by-one error!
        target = df.iloc[i + forecast_horizon - 1][target_col]
        
        # The date should correspond to the PREDICTION date, not feature date
        # DEFECT: This is also wrong - should be forecast_horizon steps ahead
        pred_date = df.iloc[i + forecast_horizon - 1][config.DATE_COLUMN]
        
        X_list.append(features)
        y_list.append(target)
        date_list.append(pred_date)
    
    X = np.array(X_list)
    y = np.array(y_list)
    dates = pd.DatetimeIndex(date_list)
    
    return X, y, dates


def get_chronological_splits(
    df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    CORRECT implementation: Chronological split (for oracle solution).
    This is the CORRECT way that agents should implement.
    """
    total_days = len(df)
    
    # Proper chronological split
    train_end = config.TRAIN_DAYS
    val_end = train_end + config.VAL_DAYS
    
    train_df = df.iloc[:train_end].copy()
    val_df = df.iloc[train_end:val_end].copy()
    test_df = df.iloc[val_end:].copy()
    
    return train_df, val_df, test_df
