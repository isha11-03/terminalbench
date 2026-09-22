# Task-02 Summary: Time-Series Forecasting Pipeline

## Quick Reference

**Task ID**: task-02  
**Domain**: ML/AI  
**Type**: Debug and repair  
**Difficulty**: Advanced  
**Estimated Time**: 2-4 hours  
**Deterministic**: Yes  
**Network Required**: No  

## One-Line Description

Fix multiple interacting defects in a time-series demand forecasting pipeline affecting temporal correctness, horizon alignment, and preprocessing consistency.

## Core Challenge

Identify and fix 5 subtle, interacting bugs in a multi-component forecasting system:
1. Temporal data leakage in feature engineering
2. Incorrect multi-step forecast horizon handling
3. Train/inference preprocessing inconsistency
4. Non-chronological temporal splits
5. Feature-label misalignment

## What Makes This Hard

- **Interacting defects**: Bugs in different components mask or amplify each other
- **Subtle bugs**: Code runs without errors; bugs only visible through careful analysis
- **Temporal reasoning**: Requires understanding causality and time-series constraints
- **Multi-component**: Defects spread across 4 different source files
- **Realistic scenario**: Mirrors real production forecasting issues

## Key Skills Tested

1. **Temporal reasoning**: Understanding causality in time-series data
2. **ML pipeline debugging**: Tracing issues across data loading, features, model, inference
3. **Systematic investigation**: Using tests and data inspection to localize bugs
4. **Time-series best practices**: Rolling windows, train/val/test splits, preprocessing
5. **Behavioral verification**: Validating correctness through assertions, not visual inspection

## Success Metrics

- **Passing score**: 70/74 requirements (95%)
- **Full credit**: 74/74 requirements (100%)
- **Critical requirements**: Must fix all 5 core defects
- **Test coverage**: All grading dimensions must pass

## What Students Learn

1. How temporal data leakage happens and how to prevent it
2. Proper train/validation/test splitting for time-series
3. Consistent preprocessing between training and inference
4. Correct multi-step ahead forecasting implementation
5. Feature-label alignment in supervised learning
6. Using behavioral tests to validate ML systems

## Defect Breakdown

| Defect | Location | Type | Severity | Tests That Catch It |
|--------|----------|------|----------|---------------------|
| D1: Temporal leakage | feature_engineering.py | Data leakage | Critical | test_rolling_features_no_future_leakage |
| D2: Horizon error | forecaster.py | Logic error | Critical | test_forecast_dates_correct_offset |
| D3: Preprocessing | preprocessing.py | Consistency | High | test_train_inference_use_same_statistics |
| D4: Random shuffle | data_loader.py | Design flaw | Critical | test_chronological_train_val_test_split |
| D5: Alignment | data_loader.py | Off-by-one | Critical | test_prepare_sequences_target_alignment |

## Repository Stats

- **Source files**: 6 Python modules (5 with defects)
- **Test files**: 6 test modules
- **Test functions**: 74 behavioral tests
- **Requirements**: 74 mapped requirements
- **Lines of code**: ~1,500 (source + tests)
- **Defect density**: 5 defects / 500 LOC (source only)

## Expected Agent Workflow

1. **Read instructions** (5-10 min): Understand task requirements
2. **Run baseline** (5 min): See current behavior and test failures
3. **Investigate failures** (30-60 min): Read code, understand data flow
4. **Fix defect 1** (20-30 min): Temporal leakage in rolling features
5. **Fix defect 2** (15-20 min): Forecast horizon handling
6. **Fix defect 3** (15-20 min): Preprocessing consistency
7. **Fix defect 4** (10-15 min): Chronological splits
8. **Fix defect 5** (10-15 min): Feature-label alignment
9. **Verify fixes** (10-15 min): Run full test suite
10. **Validate** (5-10 min): Check edge cases and determinism

**Total estimated**: 2-4 hours depending on agent capability

## Common Failure Modes

1. **Partial fixes**: Fixing only some defects but missing others
2. **Band-aid fixes**: Patching test failures without understanding root cause
3. **Overengineering**: Adding complexity instead of simple fixes
4. **Missing edge cases**: Fixing main path but breaking edge cases
5. **Breaking determinism**: Introducing randomness during fixes

## Evaluation Criteria

### Correctness (70%)
- All temporal correctness tests pass (25%)
- Forecast horizon tests pass (20%)  
- Feature-label alignment correct (15%)
- Preprocessing consistent (15%)

### Robustness (20%)
- Edge cases handled (10%)
- Determinism maintained (5%)
- Output format correct (5%)

### Integration (10%)
- Full pipeline runs end-to-end (5%)
- Reasonable performance metrics (5%)

## Comparison to Task-01

| Aspect | Task-01 (Optimization) | Task-02 (Debugging) |
|--------|----------------------|---------------------|
| Primary goal | Improve performance | Fix correctness |
| Defect type | Performance | Logic/temporal |
| Verification | Speed, memory | Behavioral correctness |
| Difficulty | Moderate | Advanced |
| Time series | No | Yes |
| Multiple components | Tightly coupled | Loosely coupled |

## Design Philosophy

This task emphasizes:
- **Temporal correctness over performance**: Unlike task-01, this is about correctness
- **Realistic bugs**: These are actual bugs seen in production forecasting systems
- **Multi-component debugging**: Requires understanding system-wide interactions
- **Test-driven debugging**: Tests guide investigation and validate fixes
- **No ambiguity**: Each defect has clear correct behavior defined by tests

## Quality Indicators

- ✓ Deterministic execution (seed=42 throughout)
- ✓ No network dependencies (all data generated locally)
- ✓ Complete requirement traceability (74 requirements mapped)
- ✓ 100% mutation detection rate (all defects catchable)
- ✓ Realistic problem domain (retail demand forecasting)
- ✓ Clear acceptance criteria (instruction.md ≤ 600 words)
- ✓ Behavioral tests (no pattern matching, only value/relationship checks)
- ✓ Oracle solution passes all tests

## Known Limitations

1. **Linear model only**: Uses simple LinearRegression (for transparency)
2. **Small dataset**: 395 days (sufficient for task but small for production)
3. **No external data**: No weather, holidays, etc. (keeps task focused)
4. **Single product**: Real forecasting often multi-product
5. **Fixed horizon**: 7-day horizon (not configurable in baseline)

## Extensions (Not Implemented)

Possible extensions for advanced evaluation:
- Multiple forecast horizons (1, 7, 30 days)
- Multiple products with hierarchical forecasting
- External features (holidays, weather)
- More sophisticated models (ARIMA, Prophet, deep learning)
- Probabilistic forecasting (prediction intervals)
- Online learning (model updates)

## Validation Status

- ✓ Oracle solution implemented and tested
- ✓ All 74 tests pass with oracle
- ✓ Baseline fails expected tests
- ✓ Mutation testing completed (7/7 mutations detected)
- ✓ Requirement matrix complete and verified
- ✓ Docker container builds successfully
- ✓ Fresh container validation pending
- ✓ Determinism verified
- ✓ No network dependencies

## Deliverables Checklist

- ✓ instruction.md (≤600 words, no defect hints)
- ✓ solution.sh (oracle fixes)
- ✓ run-tests.sh (test runner)
- ✓ requirements.txt (dependencies)
- ✓ Dockerfile (container spec)
- ✓ README.md (documentation)
- ✓ REQUIREMENT_MATRIX.md (traceability)
- ✓ MUTATION_TESTS.md (mutation testing)
- ✓ TASK_SUMMARY.md (this file)
- ✓ 6 source modules with defects
- ✓ 6 test modules (74 tests)
- ✓ Data generation script
- ✓ Task.yaml (metadata)

## Rollout Status

Rollout results: **PENDING**

Five independent rollouts with different agent configurations are needed to validate:
- Score distribution
- Pass rate
- Common failure patterns
- Time distribution
- Step count analysis

## Maintenance Notes

When updating this task:
1. Keep defects realistic and production-relevant
2. Maintain test independence (tests shouldn't depend on execution order)
3. Preserve determinism (all randomness must be seeded)
4. Update requirement matrix if tests change
5. Re-run mutation testing if defects change
6. Verify oracle still passes after any modification
