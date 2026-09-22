# Task: Time-Series Demand Forecasting Pipeline

Repair the deterministic retail demand forecasting pipeline in this directory. It loads historical demand with price, promotions, and calendar features; engineers lag and rolling features; creates chronological train/validation/test splits; trains a linear model; and produces seven-day forecasts.

The implementation contains interacting temporal defects. Inspect the data loader, feature engineering, preprocessing, forecaster, and orchestration code. Ensure no future values leak into past features or training data, chronological ordering is preserved, features and labels are aligned, and training and inference use identical normalization statistics. Forecast dates and seven-day horizon semantics must be correct.

Preserve existing public pipeline interfaces. Handle missing values, cold-start rows, and split boundaries. Results must be numerically valid and deterministic across repeated runs. Use only local files and dependencies; do not modify tests, generated data, or data-generation logic.

Run `./run-tests.sh` to observe failures and rerun it after each repair. Leave the source pipeline production-ready with all behavioral tests passing.
