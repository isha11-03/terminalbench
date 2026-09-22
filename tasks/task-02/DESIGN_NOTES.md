# Task-02 Design: Time-Series Demand Forecasting Pipeline

## Problem Overview

**Domain**: Retail demand forecasting for inventory planning  
**Task**: Multi-step ahead demand forecasting (7-day horizon)  
**Data**: Daily product demand with external features (price, promotions, day-of-week)

## Realistic Interacting Defects (Hidden from Agent)

### Defect 1: Temporal Contamination (Data Leakage)
**Location**: Feature engineering in `src/feature_engineering.py`
- Rolling statistics (mean, std) computed over **entire dataset** including future data
- Lag features created incorrectly, allowing future data to leak into features
- Impact: Artificially inflated accuracy on validation, fails in production

### Defect 2: Incorrect Forecast Horizon Handling
**Location**: Forecasting logic in `src/forecaster.py`
- Multi-step forecast uses wrong indexing for future predictions
- Recursive forecasting doesn't properly shift the feature window
- Off-by-one errors in date alignment for forecast output
- Impact: Predictions misaligned with target dates

### Defect 3: Train/Inference Preprocessing Inconsistency
**Location**: Preprocessing in `src/preprocessing.py` and `src/forecaster.py`
- Training uses fit_transform() on full dataset (leaks statistics)
- Inference uses different normalization (creates distribution shift)
- Missing value handling differs between train and test
- Impact: Model sees inconsistent feature distributions

### Defect 4: Improper Temporal Train/Val Split
**Location**: Data splitting in `src/data_loader.py`
- Uses random shuffle instead of chronological split
- Validation data contains samples from before training data
- Impact: Invalid evaluation, overly optimistic metrics

### Defect 5: Feature-Label Alignment Error
**Location**: Dataset preparation in `src/data_loader.py`
- Features and labels misaligned by 1-2 timesteps
- Forecast target computation uses wrong offset
- Impact: Model learns wrong temporal relationships

## Grading Dimensions

1. **Temporal Correctness** (25%)
   - No future data leakage in features
   - Chronological train/val/test splits
   - Proper temporal causality

2. **Forecast Horizon Correctness** (20%)
   - Predictions aligned with correct future dates
   - Multi-step forecasting produces exactly N steps ahead
   - Date indexing correct

3. **Feature/Label Alignment** (15%)
   - Features and targets properly synchronized
   - Lag features computed correctly
   - No off-by-one errors

4. **Preprocessing Consistency** (15%)
   - Train and inference use same normalization statistics
   - Missing value handling consistent
   - No data leakage in preprocessing

5. **Edge Cases** (10%)
   - Handles missing values in features
   - Handles cold start (insufficient history)
   - Handles edge dates correctly

6. **Forecast Output Correctness** (10%)
   - Output format matches specification
   - All required fields present
   - Predictions are numeric and valid

7. **Determinism** (5%)
   - Reproducible results with same seed
   - No randomness in data loading or feature generation

## Data Characteristics

- **Duration**: 365 days historical + 30 days test
- **Frequency**: Daily
- **Features**:
  - demand (target)
  - price (continuous)
  - promotion (binary)
  - day_of_week (categorical)
  - rolling statistics (to be computed)
  - lag features (to be computed)

- **Patterns**:
  - Weekly seasonality
  - Price elasticity
  - Promotion effects
  - Trend component

## Test Strategy

### Correctness Tests
- Verify no temporal leakage (future data not in past features)
- Verify chronological splits
- Verify forecast dates match expected horizon
- Verify feature-label alignment

### Behavioral Tests
- End-to-end forecasting produces valid predictions
- Train/inference consistency
- Edge case handling (missing data, cold start)

### Determinism Tests
- Multiple runs produce identical results
- Reproducible with fixed seed

## Oracle Solution Requirements

Must fix all defects:
1. Compute rolling statistics only on past data (expanding/rolling windows)
2. Fix forecast horizon indexing and date alignment
3. Ensure train/inference use same preprocessing statistics
4. Implement proper chronological splitting
5. Correct feature-label alignment

## Success Criteria

Agent must:
1. Identify temporal leakage and fix rolling statistics
2. Fix forecast horizon and date alignment
3. Ensure preprocessing consistency
4. Fix temporal splitting logic
5. Correct feature-label alignment
6. Pass all behavioral tests
7. Maintain determinism

## Repository Structure

```
task-02/
├── data/
│   └── generate_data.py          # Deterministic data generation
├── src/
│   ├── __init__.py
│   ├── data_loader.py            # Defect 4, 5: Split and alignment
│   ├── preprocessing.py          # Defect 3: Inconsistent preprocessing
│   ├── feature_engineering.py    # Defect 1: Temporal leakage
│   ├── forecaster.py             # Defect 2, 3: Horizon and preprocessing
│   └── config.py                 # Configuration
├── tests/
│   ├── test_temporal_correctness.py
│   ├── test_forecast_horizon.py
│   ├── test_preprocessing.py
│   ├── test_edge_cases.py
│   ├── test_determinism.py
│   └── test_integration.py
├── instruction.md
├── solution.sh
├── run-tests.sh
└── requirements.txt
```

## Mutation Testing Targets

1. Remove temporal leakage fix → tests should fail
2. Reintroduce horizon error → forecast dates wrong
3. Break preprocessing consistency → different train/inference stats
4. Use random split → temporal correctness tests fail
5. Reintroduce alignment error → predictions shifted

