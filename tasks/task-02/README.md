# Task-02: Time-Series Demand Forecasting Pipeline

## Overview

This task presents a demand forecasting pipeline with multiple interacting defects affecting temporal correctness, forecast horizon handling, preprocessing consistency, and feature-label alignment. The repository contains a complete ML pipeline for retail demand forecasting with realistic bugs that violate time-series best practices.

**Domain**: ML/AI - Time-Series Forecasting  
**Difficulty**: Advanced (requires understanding of temporal causality, ML pipelines, and debugging)  
**Estimated Time**: 2-4 hours

## Problem Description

You're given a forecasting system that predicts retail demand 7 days ahead. The pipeline includes:
- Historical demand data with external features (price, promotions, day-of-week)
- Feature engineering (lag features, rolling statistics, date features)
- Temporal train/validation/test splitting
- Linear regression model
- Multi-step ahead forecasting

The system runs and produces seemingly reasonable results, but contains **5 interacting defects** that violate temporal correctness, misalign predictions, and create data leakage. These issues make it unsuitable for production despite decent-looking validation metrics.

## Repository Structure

```
task-02/
├── data/
│   ├── __init__.py
│   └── generate_data.py           # Deterministic data generation
├── src/
│   ├── __init__.py
│   ├── config.py                  # Configuration parameters
│   ├── data_loader.py             # Data loading and splitting [DEFECT 4, 5]
│   ├── preprocessing.py           # Normalization [DEFECT 3]
│   ├── feature_engineering.py     # Feature creation [DEFECT 1]
│   ├── forecaster.py              # Forecasting model [DEFECT 2, 3]
│   └── pipeline.py                # Main orchestration
├── tests/
│   ├── test_temporal_correctness.py   # Temporal causality tests
│   ├── test_forecast_horizon.py       # Horizon alignment tests
│   ├── test_preprocessing.py          # Preprocessing consistency tests
│   ├── test_edge_cases.py             # Edge case handling
│   ├── test_determinism.py            # Reproducibility tests
│   └── test_integration.py            # End-to-end tests
├── instruction.md                 # Task instructions
├── solution.sh                    # Oracle solution (fixes all defects)
├── run-tests.sh                   # Test runner
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container specification
├── REQUIREMENT_MATRIX.md          # Requirement-to-test mapping
├── MUTATION_TESTS.md              # Mutation testing results
└── README.md                      # This file
```

## Defects (Hidden from Task Description)

The following defects are deliberately introduced but NOT revealed in `instruction.md`:

1. **Temporal Contamination**: Rolling statistics computed with `center=True`, causing future data to leak into past features
2. **Incorrect Forecast Horizon**: Off-by-one errors in multi-step forecasting and date alignment
3. **Preprocessing Inconsistency**: Training and inference use different normalization statistics
4. **Improper Temporal Split**: Random shuffle instead of chronological ordering in train/val/test splits
5. **Feature-Label Misalignment**: Features and targets are off by one timestep

## Getting Started

### Prerequisites

- Python 3.8+
- pip or conda

### Setup

1. Generate the data:
```bash
python3 data/generate_data.py
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the baseline pipeline:
```bash
python3 -m src.pipeline
```

4. Run tests to see what fails:
```bash
./run-tests.sh
```

### Docker (Recommended for Evaluation)

```bash
# Build the container
docker build -t task-02 .

# Run tests
docker run task-02 ./run-tests.sh

# Run solution
docker run task-02 bash -c "./solution.sh && ./run-tests.sh"
```

## Expected Baseline Behavior

The baseline implementation (with all defects) should:
- Run without crashing
- Produce forecasts
- Show decent validation metrics (artificially inflated due to data leakage)
- **FAIL** critical tests related to temporal correctness, horizon alignment, and preprocessing

## Expected Oracle Behavior

After running `solution.sh`, the implementation should:
- Pass **all 74 test requirements**
- Maintain deterministic behavior
- Respect temporal causality
- Produce correctly aligned forecasts
- Use consistent preprocessing

## Test Suite

The test suite includes 6 test files with 74 behavioral requirements:

- **test_temporal_correctness.py** (10 tests): Verifies no future data leakage, chronological splits
- **test_forecast_horizon.py** (9 tests): Verifies correct date alignment for multi-step forecasts
- **test_preprocessing.py** (10 tests): Verifies train/inference consistency
- **test_edge_cases.py** (14 tests): Verifies boundary conditions and missing data handling
- **test_determinism.py** (9 tests): Verifies reproducibility
- **test_integration.py** (11 tests): Verifies end-to-end functionality

Run specific test files:
```bash
python3 -m pytest tests/test_temporal_correctness.py -v
python3 -m pytest tests/test_forecast_horizon.py -v
```

## Grading Dimensions

1. **Temporal Correctness** (25%): No future data leakage, chronological splits maintained
2. **Forecast Horizon Correctness** (20%): Multi-step predictions correctly aligned with target dates
3. **Feature-Label Alignment** (15%): Features and labels properly synchronized
4. **Preprocessing Consistency** (15%): Train and inference use same normalization
5. **Edge Cases** (10%): Missing values, boundaries handled correctly
6. **Forecast Output Correctness** (10%): Valid numeric predictions
7. **Determinism** (5%): Reproducible results
8. **Integration** (10%): End-to-end functionality

## Key Files

- **instruction.md**: The task prompt given to agents (≤600 words, no defect hints)
- **solution.sh**: Oracle solution that fixes all defects
- **REQUIREMENT_MATRIX.md**: Maps 74 requirements to tests and oracle
- **MUTATION_TESTS.md**: Documents mutation testing results

## Validation

### Baseline Tests (Expected Failures)

```bash
# Should fail temporal correctness tests
python3 -m pytest tests/test_temporal_correctness.py::TestTemporalCorrectness::test_chronological_train_val_test_split -v

# Should fail rolling feature tests
python3 -m pytest tests/test_temporal_correctness.py::TestTemporalCorrectness::test_rolling_features_no_future_leakage -v

# Should fail horizon tests
python3 -m pytest tests/test_forecast_horizon.py::TestForecastHorizon::test_forecast_dates_correct_offset -v
```

### Oracle Tests (Expected Pass)

```bash
# Apply fixes
./solution.sh

# Run all tests
./run-tests.sh
# Expected: All tests pass
```

## Data Characteristics

The synthetic demand data includes:
- **395 days**: 300 training, 65 validation, 30 test
- **Features**: demand (target), price, promotion, day_of_week
- **Patterns**: Weekly seasonality, price elasticity, promotion effects, upward trend
- **Deterministic**: Seed=42, fully reproducible

## Common Pitfalls

1. **Temporal Leakage**: Rolling statistics that look forward
2. **Date Misalignment**: Off-by-one errors in forecast dates
3. **Distribution Shift**: Different preprocessing stats in train vs inference
4. **Data Snooping**: Validation data chronologically before training data
5. **Index Errors**: Features and labels not properly aligned

## Success Criteria

A correct solution must:
1. ✓ Pass all 74 test requirements
2. ✓ Maintain chronological train/val/test splits
3. ✓ Use only past data in rolling statistics
4. ✓ Align forecast dates correctly (1, 2, ..., N days ahead)
5. ✓ Use consistent preprocessing between train and inference
6. ✓ Properly align features and labels
7. ✓ Produce deterministic results

## Debugging Tips

1. **Start with temporal correctness**: Fix chronological splits first
2. **Check feature engineering**: Verify rolling statistics use `center=False`
3. **Inspect date alignment**: Print forecast dates and verify offsets
4. **Test preprocessing**: Ensure fitted statistics are reused
5. **Validate alignment**: Check that features at time t predict target at time t+h

## Performance

The corrected implementation should have:
- **Validation MAE**: ~15-25 (depends on split and features)
- **Test MAE**: ~15-25
- **Inference time**: <1 second for 7-day forecast
- **Memory**: <100MB

Note: Validation metrics may be *worse* after fixing data leakage (this is expected and correct).

## Contributing

This is a benchmark task. Do not modify:
- Test specifications
- Data generation logic
- Task requirements

## License

This task is part of the Terminal Bench benchmark suite.

## Contact

For questions about this task, refer to the main benchmark documentation.
