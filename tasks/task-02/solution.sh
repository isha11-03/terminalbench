#!/bin/bash
# Oracle solution for TASK-02: Time-Series Forecasting Pipeline
# Fixes all 5 defects in the baseline implementation

set -e

echo "Applying fixes to forecasting pipeline..."

# Fix 1: Remove temporal contamination in rolling statistics (center=True -> center=False)
echo "Fix 1: Removing temporal leakage from rolling features..."
cat > src/feature_engineering.py << 'EOF'
"""
Feature engineering for time-series forecasting.

FIXED: Temporal contamination in rolling statistics removed.
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
    
    FIXED: Use center=False (default) to only look backward.
    This ensures no future data leakage.
    """
    if windows is None:
        windows = config.ROLLING_WINDOWS
    
    df = df.copy()
    
    for window in windows:
        # FIXED: Use .rolling() with center=False (default) to only look backward
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
    
    FIXED: Now uses corrected rolling features.
    """
    df = df.copy()
    
    # Lag features (correct)
    df = create_lag_features(df)
    
    # Rolling features (FIXED: no temporal leakage)
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
EOF

# Fix 2: Use chronological split instead of random shuffle
echo "Fix 2: Fixing temporal split to be chronological..."
cat > src/data_loader.py << 'EOF'
"""
Data loading and temporal splitting.

FIXED: All defects corrected.
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
    
    FIXED: Uses proper chronological splitting, respecting temporal causality.
    
    Args:
        df: Full dataset
        
    Returns:
        train_df, val_df, test_df
    """
    total_days = len(df)
    
    # FIXED: Proper chronological split - no shuffling!
    train_end = config.TRAIN_DAYS
    val_end = train_end + config.VAL_DAYS
    
    train_df = df.iloc[:train_end].copy()
    val_df = df.iloc[train_end:val_end].copy()
    test_df = df.iloc[val_end:].copy()
    
    return train_df, val_df, test_df


def prepare_sequences(
    df: pd.DataFrame,
    feature_cols: list,
    target_col: str = config.TARGET_COLUMN,
    forecast_horizon: int = config.FORECAST_HORIZON
) -> Tuple[np.ndarray, np.ndarray, pd.DatetimeIndex]:
    """
    Prepare feature sequences and targets for forecasting.
    
    FIXED: Correct feature-label alignment.
    
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
        # FIXED: Take features at time i
        features = df.iloc[i][feature_cols].values
        
        # FIXED: Take target at time i + forecast_horizon (correct offset)
        target = df.iloc[i + forecast_horizon][target_col]
        
        # FIXED: The date corresponds to the PREDICTION date
        pred_date = df.iloc[i + forecast_horizon][config.DATE_COLUMN]
        
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
EOF

# Fix 3: Fix preprocessing to use fit_data parameter and ensure consistency
echo "Fix 3: Fixing preprocessing consistency..."
cat > src/preprocessing.py << 'EOF'
"""
Data preprocessing and normalization.

FIXED: Preprocessing consistency corrected.
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional


class DataPreprocessor:
    """
    Handles data preprocessing including normalization and missing value handling.
    
    FIXED: Training and inference now use consistent statistics.
    """
    
    def __init__(self):
        self.feature_means_ = None
        self.feature_stds_ = None
        self.fitted_ = False
    
    def fit_transform(self, X: np.ndarray, fit_data: np.ndarray = None) -> np.ndarray:
        """
        Fit preprocessing on data and transform.
        
        FIXED: Now correctly uses fit_data parameter if provided.
        
        Args:
            X: Data to transform
            fit_data: Data to fit statistics on (if None, uses X)
            
        Returns:
            Transformed data
        """
        # FIXED: Use fit_data if provided, otherwise use X
        data_to_fit = fit_data if fit_data is not None else X
        
        self.feature_means_ = np.mean(data_to_fit, axis=0)
        self.feature_stds_ = np.std(data_to_fit, axis=0)
        self.feature_stds_[self.feature_stds_ == 0] = 1.0  # Avoid division by zero
        self.fitted_ = True
        
        # Normalize using fitted statistics
        X_normalized = (X - self.feature_means_) / self.feature_stds_
        
        return X_normalized
    
    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform data using fitted statistics.
        
        FIXED: Now requires fitting first.
        """
        if not self.fitted_:
            raise ValueError("Preprocessor must be fitted before transform. Call fit_transform first.")
        
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
        
        FIXED: Consistent missing value handling.
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
EOF

# Fix 4: Fix forecast horizon handling and date alignment
echo "Fix 4: Fixing forecast horizon handling..."
cat > src/forecaster.py << 'EOF'
"""
Demand forecasting model.

FIXED: All defects corrected.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from typing import Dict, List, Tuple
from . import config
from .preprocessing import DataPreprocessor
from .feature_engineering import get_feature_columns


class DemandForecaster:
    """
    Demand forecasting model with multi-step ahead predictions.
    
    FIXED: Preprocessing and forecasting defects corrected.
    """
    
    def __init__(self, random_seed: int = config.RANDOM_SEED):
        self.model = LinearRegression()
        self.preprocessor = DataPreprocessor()
        self.random_seed = random_seed
        self.feature_cols = None
        self.is_trained = False
    
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        feature_cols: List[str]
    ):
        """
        Train the forecasting model.
        
        FIXED: Preprocessing now correctly fits on training data only.
        """
        self.feature_cols = feature_cols
        
        # FIXED: Correctly fit preprocessor on training data
        X_train_normalized = self.preprocessor.fit_transform(X_train)
        
        # Train model
        self.model.fit(X_train_normalized, y_train)
        self.is_trained = True
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions on input features.
        
        FIXED: Uses fitted preprocessor consistently.
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # FIXED: transform() now requires fitting first
        X_normalized = self.preprocessor.transform(X)
        
        predictions = self.model.predict(X_normalized)
        
        return predictions
    
    def forecast_multi_step(
        self,
        df: pd.DataFrame,
        start_date: pd.Timestamp,
        horizon: int = config.FORECAST_HORIZON
    ) -> Dict[str, List]:
        """
        Generate multi-step ahead forecast.
        
        FIXED: Correct forecast horizon handling and date alignment.
        
        Args:
            df: DataFrame with features up to start_date
            start_date: Date to start forecasting from
            horizon: Number of days to forecast ahead
            
        Returns:
            Dictionary with 'dates' and 'predictions'
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before forecasting")
        
        # Find the starting point in the dataframe
        start_idx = df[df[config.DATE_COLUMN] == start_date].index
        if len(start_idx) == 0:
            raise ValueError(f"Start date {start_date} not found in data")
        start_idx = start_idx[0]
        
        forecast_dates = []
        forecast_values = []
        
        # FIXED: Correct horizon handling
        for i in range(horizon):
            # FIXED: Correct index calculation (start from next day)
            current_idx = start_idx + i + 1
            
            if current_idx >= len(df):
                break
            
            # FIXED: Date is correctly aligned
            forecast_date = df.iloc[current_idx][config.DATE_COLUMN]
            
            # Extract features for the point we're forecasting from
            # We need features from an earlier point that can predict this date
            feature_idx = start_idx + i
            if feature_idx >= len(df):
                break
                
            features = df.iloc[feature_idx][self.feature_cols].values.reshape(1, -1)
            
            # Make prediction
            pred = self.predict(features)[0]
            
            forecast_dates.append(forecast_date)
            forecast_values.append(pred)
        
        return {
            'dates': forecast_dates,
            'predictions': forecast_values
        }
    
    def evaluate(
        self,
        X_val: np.ndarray,
        y_val: np.ndarray
    ) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        This is correct - no defects here.
        """
        predictions = self.predict(X_val)
        
        # Calculate metrics
        mae = np.mean(np.abs(predictions - y_val))
        rmse = np.sqrt(np.mean((predictions - y_val) ** 2))
        mape = np.mean(np.abs((y_val - predictions) / y_val)) * 100
        
        return {
            'mae': mae,
            'rmse': rmse,
            'mape': mape
        }
EOF

echo "All fixes applied successfully!"
echo ""
echo "Summary of fixes:"
echo "1. Rolling statistics now use center=False (backward-looking only)"
echo "2. Temporal splits are now chronological (no random shuffle)"
echo "3. Preprocessing is now consistent between train and inference"
echo "4. Forecast horizon handling corrected with proper date alignment"
echo "5. Feature-label alignment fixed (correct offset)"
echo ""
echo "Running tests to verify fixes..."
