"""
Feature engineering for time-series forecasting.

DEFECT:
- Defect 1: Temporal contamination in rolling statistics (lines 45-80)
"""

import pandas as pd
import numpy as np
from typing import List
from . import config


def create_lag_features(
    df: pd.DataFrame,
    target_col: str = config.TARGET_COLUMN,
    lags: List[int] = None
) -> pd.DataFrame:
    """
    Create lag features (past values).
    
    This implementation is CORRECT - no defects here.
    """
    if lags is None:
        lags = config.LAG_FEATURES
    
    df = df.copy()
    
    for lag in lags:
        df[f'demand_lag_{lag}'] = df[target_col].shift(lag)
    
    return df


def create_rolling_features(
    df: pd.DataFrame,
    target_col: str = config.TARGET_COLUMN,
    windows: List[int] = None
) -> pd.DataFrame:
    """
    Create rolling statistics features.
    
    DEFECT 1: TEMPORAL CONTAMINATION - computes rolling statistics
    over the entire dataset including FUTURE data, causing massive
    data leakage that inflates validation performance artificially.
    
    This is a subtle but critical bug that makes the model see future
    information it shouldn't have access to at prediction time.
    """
    if windows is None:
        windows = config.ROLLING_WINDOWS
    
    df = df.copy()
    
    for window in windows:
        # DEFECT: Using .rolling() on the full series WITHOUT proper
        # temporal awareness causes it to include future data!
        # The correct approach would be to use expanding windows or
        # ensure rolling windows only look backward.
        
        # CRITICAL BUG: This computes mean/std over future data!
        # At time t, this includes data from t-window to t+window
        df[f'demand_rolling_mean_{window}'] = (
            df[target_col].rolling(window=window, center=True).mean()
        )
        
        df[f'demand_rolling_std_{window}'] = (
            df[target_col].rolling(window=window, center=True).std()
        )
        
        # Also create min/max for diversity
        df[f'demand_rolling_min_{window}'] = (
            df[target_col].rolling(window=window, center=True).min()
        )
        
        df[f'demand_rolling_max_{window}'] = (
            df[target_col].rolling(window=window, center=True).max()
        )
    
    return df


def create_date_features(df: pd.DataFrame, date_col: str = config.DATE_COLUMN) -> pd.DataFrame:
    """
    Create date-based features.
    
    This implementation is CORRECT - no defects here.
    """
    df = df.copy()
    
    # Already have day_of_week from raw data, but create additional features
    df['day_of_month'] = df[date_col].dt.day
    df['month'] = df[date_col].dt.month
    df['quarter'] = df[date_col].dt.quarter
    df['week_of_year'] = df[date_col].dt.isocalendar().week
    
    # Is weekend flag
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    return df


def create_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create all engineered features.
    
    DEFECT 1 is propagated through this function via create_rolling_features.
    """
    df = df.copy()
    
    # Lag features (correct)
    df = create_lag_features(df)
    
    # Rolling features (DEFECT: temporal leakage here!)
    df = create_rolling_features(df)
    
    # Date features (correct)
    df = create_date_features(df)
    
    return df


def get_feature_columns(df: pd.DataFrame) -> List[str]:
    """Get list of all feature columns (excluding date and target)."""
    exclude = [config.DATE_COLUMN, config.TARGET_COLUMN]
    feature_cols = [col for col in df.columns if col not in exclude]
    return feature_cols


def create_rolling_features_correct(
    df: pd.DataFrame,
    target_col: str = config.TARGET_COLUMN,
    windows: List[int] = None
) -> pd.DataFrame:
    """
    CORRECT implementation using expanding windows for oracle solution.
    This is what agents should implement to fix Defect 1.
    """
    if windows is None:
        windows = config.ROLLING_WINDOWS
    
    df = df.copy()
    
    for window in windows:
        # CORRECT: Use .rolling() with center=False (default) to only look backward
        # This ensures no future data leakage
        df[f'demand_rolling_mean_{window}'] = (
            df[target_col].rolling(window=window, min_periods=1).mean()
        )
        
        df[f'demand_rolling_std_{window}'] = (
            df[target_col].rolling(window=window, min_periods=1).std()
        )
        
        df[f'demand_rolling_min_{window}'] = (
            df[target_col].rolling(window=window, min_periods=1).min()
        )
        
        df[f'demand_rolling_max_{window}'] = (
            df[target_col].rolling(window=window, min_periods=1).max()
        )
    
    return df
