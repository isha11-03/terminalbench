"""
Demand forecasting model.

DEFECTS:
- Defect 2: Incorrect forecast horizon handling (lines 95-140)
- Defect 3: Preprocessing inconsistency (lines 55-70)
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
    
    Contains multiple interacting defects in preprocessing and forecasting logic.
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
        
        DEFECT 3: Preprocessing leakage - fits preprocessor on training
        data but the preprocessor has a bug that may leak information.
        """
        self.feature_cols = feature_cols
        
        # DEFECT 3: The fit_transform call has a bug in preprocessing.py
        # that ignores the fit_data parameter, but even if it didn't,
        # we're not using it correctly here
        X_train_normalized = self.preprocessor.fit_transform(X_train)
        
        # Train model
        self.model.fit(X_train_normalized, y_train)
        self.is_trained = True
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions on input features.
        
        DEFECT 3: If preprocessor wasn't fitted properly, transform()
        will compute statistics on inference data (distribution shift).
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # DEFECT 3: transform() has a bug that uses inference data stats
        # if preprocessor wasn't fitted, creating inconsistency
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
        
        DEFECT 2: INCORRECT FORECAST HORIZON HANDLING
        - Wrong indexing for future predictions
        - Forecast dates misaligned with predictions
        - Off-by-one errors in date calculation
        
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
        
        # DEFECT 2: Incorrect horizon handling!
        # This loop has multiple bugs:
        for i in range(horizon):
            # BUG 1: Wrong index calculation
            # Should be start_idx + i + 1, but is start_idx + i
            current_idx = start_idx + i
            
            if current_idx >= len(df):
                break
            
            # BUG 2: Date calculation is off by one
            # We want to predict 'horizon' days ahead, but this predicts
            # at the wrong dates
            forecast_date = df.iloc[current_idx][config.DATE_COLUMN]
            
            # Extract features for this timestep
            features = df.iloc[current_idx][self.feature_cols].values.reshape(1, -1)
            
            # Make prediction
            pred = self.predict(features)[0]
            
            forecast_dates.append(forecast_date)
            forecast_values.append(pred)
        
        # DEFECT 2: The returned dates don't match the actual forecast horizon
        # If start_date is '2023-12-25' and horizon is 7, we should return
        # predictions for 2023-12-26 through 2024-01-01, but due to bugs above,
        # we return wrong dates
        
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
