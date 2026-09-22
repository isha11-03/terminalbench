"""Configuration for forecasting pipeline."""

# Data configuration
DATA_PATH = "demand_data.csv"
DATE_COLUMN = "date"
TARGET_COLUMN = "demand"

# Temporal split configuration
TRAIN_DAYS = 300  # First 300 days for training
VAL_DAYS = 65     # Next 65 days for validation
TEST_DAYS = 30    # Last 30 days for testing

# Feature engineering configuration
LAG_FEATURES = [1, 7, 14]  # Lag by 1 day, 1 week, 2 weeks
ROLLING_WINDOWS = [7, 14, 28]  # Rolling statistics windows

# Forecasting configuration
FORECAST_HORIZON = 7  # Predict 7 days ahead
RANDOM_SEED = 42

# Model configuration
MODEL_TYPE = "linear"  # Simple linear regression for transparency
