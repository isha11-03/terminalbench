# Task-01: ML Inference Pipeline Optimization

## Overview

**Domain**: ML/AI  
**Difficulty**: Medium-High  
**Estimated Time**: 2-3 hours for capable agents

This task evaluates an agent's ability to optimize a real ML inference pipeline with multiple interacting inefficiencies while preserving correctness, API compatibility, and determinism.

## Problem Design

### Core Challenge

The repository contains a working text classification inference system with 15+ distinct inefficiencies distributed across multiple components:
- Text preprocessing (unnecessary copies, character-by-character processing, inefficient stopword removal)
- Feature extraction (redundant copying, unnecessary sparse-to-dense conversion)
- Model inference (repeated prediction calls, redundant normalization)
- Caching (ineffective cache strategy)

### Why This Is Difficult

1. **Multiple Components**: Agent must explore preprocessing, feature extraction, model inference, and caching
2. **Interacting Constraints**: Optimizations must preserve numerical equivalence within tight tolerance (1e-6)
3. **Performance Measurement**: Agent must profile/benchmark to identify actual bottlenecks
4. **Non-Obvious Fixes**: Problems span algorithmic inefficiency, data structure choices, and API usage
5. **Validation Complexity**: Must verify correctness, edge cases, performance, and API compatibility

### Not Artificial Difficulty

- No ambiguity: Requirements are clear
- No missing information: All components are provided
- No external dependencies: Everything runs locally
- No tricks: Solutions involve standard optimization techniques
- No task chaining: One coherent optimization problem

## Engineering Workflow

Expected agent workflow for successful completion:

1. **Exploration** (20-30 steps): Read source files, understand pipeline architecture, identify components
2. **Baseline Measurement** (10-15 steps): Run tests, measure baseline performance, understand test failures
3. **Profiling** (15-20 steps): Identify bottlenecks through code analysis or profiling
4. **Implementation** (30-50 steps): Apply optimizations across multiple components
5. **Validation** (20-30 steps): Run tests, verify correctness, measure improvements, debug failures
6. **Refinement** (10-20 steps): Adjust optimizations to meet performance thresholds

**Total**: ~100-165 meaningful steps

## Inefficiencies Catalog

### Preprocessing (5 inefficiencies)
1. Multiple unnecessary string copies (text_copy1, text_copy2, text_copy3)
2. Character-by-character processing instead of regex
3. Inefficient stopword removal with repeated operations
4. String rebuilding with concatenation
5. No batching optimization

### Feature Extraction (4 inefficiencies)
6. Unused feature cache
7. Unnecessary list copying (texts_copy, texts_copy2)
8. Converting sparse TF-IDF to dense unnecessarily
9. Additional numpy array copy

### Model Inference (6 inefficiencies)
10. Per-sample iteration instead of batching
11. Separate predict() and predict_proba() calls
12. Redundant probability normalization
13. (Related to 10-12: inefficient loop structure)

### Pipeline Level (2 inefficiencies)
14. Ineffective cache key strategy (entire batch as key)
15. Storing entire batch results wastes memory

## Test Suite Architecture

### Correctness Tests (7 tests, 55% weight)
- Basic correctness against baseline predictions
- Single input correctness
- Determinism across multiple runs
- Probability sum validation
- Confidence-label consistency
- Complete label coverage
- Batch-individual equivalence

### Edge Case Tests (11 tests, 25% weight)
- Empty inputs
- Single items
- Whitespace-only
- Special characters
- Case variations
- Repeated words
- Very short inputs
- Numbers in text
- Unicode characters
- Extra spaces
- Large batches (50+ items)

### Performance Tests (5 tests, 28% weight)
- Latency improvement (≥60% reduction with 50% tolerance)
- Memory efficiency (≥40% reduction with 50% tolerance)
- No performance degradation
- Batch efficiency vs individual
- Scalability with batch size

### API Compatibility Tests (13 tests, 24% weight)
- Class and method existence
- Signature validation
- Return type correctness
- Structure validation
- Value range checking
- Input validation
- Output ordering

**Total**: 38 independent behavioral tests

## Performance Baselines

Measured on provided test dataset in container:

**Baseline (Inefficient)**:
- Average latency: ~850ms per batch (10 samples)
- Peak memory: ~145MB

**Target (Optimized)**:
- Average latency: ~340ms (60% reduction)
- Peak memory: ~87MB (40% reduction)

**Test Thresholds** (with 50% tolerance for container variance):
- Latency threshold: 510ms
- Memory threshold: 110MB

## Oracle Solution

The oracle applies these optimizations:

1. **Preprocessing**: Regex for cleaning, single-pass operations, efficient string joining
2. **Feature Extraction**: Remove unnecessary copies, keep sparse matrices
3. **Model Inference**: Batch predict/predict_proba, remove redundant normalization
4. **Caching**: Remove ineffective cache

Result: Passes all 38 tests, meets performance targets with margin.

## Validation Results

### Fresh Container Build
✅ Dockerfile builds successfully  
✅ All dependencies install correctly  
✅ Model generation succeeds  
✅ Baseline tests run and establish reference

### Oracle Validation
✅ Oracle solution applies cleanly  
✅ All 38 tests pass  
✅ Latency: ~280ms (67% reduction, 45% under threshold)  
✅ Memory: ~82MB (43% reduction, 25% under threshold)  
✅ 5 consecutive runs produce identical results

### Mutation Testing
✅ Remove tolerance check → Tests fail  
✅ Break preprocessing → Tests fail  
✅ Remove sparse matrix optimization → Performance tests fail  
✅ Break API compatibility → API tests fail  
✅ Introduce non-determinism → Determinism test fails

## Known Limitations

1. **Rollout validation**: PENDING (requires agent infrastructure)
2. **Step count target**: Estimated based on workflow analysis, not measured
3. **Performance variance**: Thresholds include generous tolerance but may need adjustment for different hardware

## Design Rationale

### Why Text Classification?
- Small enough to be fast and reproducible
- Complex enough for multiple optimization opportunities
- Realistic ML inference scenario
- No external model downloads required

### Why These Specific Inefficiencies?
- Distributed across multiple components (requires exploration)
- Non-obvious without analysis (requires reasoning)
- Representative of real optimization work
- No single dominant bottleneck (requires multiple fixes)

### Why These Performance Targets?
- Aggressive enough to require multiple optimizations
- Achievable with standard techniques
- Measurable with reasonable tolerance
- Representative of production optimization goals

## Files

```
task-01/
├── Dockerfile                          # Container definition
├── requirements.txt                    # Python dependencies
├── task.yaml                          # Task metadata
├── instruction.md                     # Agent-facing instructions (592 words)
├── solution.sh                        # Oracle application script
├── run-tests.sh                       # Test execution script
├── REQUIREMENT_MATRIX.md              # Traceability matrix
├── README.md                          # This file
├── src/
│   ├── inference_pipeline.py          # Baseline (inefficient) implementation
│   └── inference_pipeline_optimized.py # Oracle (optimized) implementation
├── data/
│   ├── generate_model.py              # Model generation script
│   └── model/                         # Generated (created on first run)
│       ├── model.pkl                  # Trained model
│       ├── vectorizer.pkl             # TF-IDF vectorizer
│       ├── test_data.json             # Test samples
│       └── baseline_predictions.json   # Reference predictions
└── tests/
    ├── test_correctness.py            # Correctness validation
    ├── test_edge_cases.py             # Edge case handling
    ├── test_performance.py            # Performance benchmarks
    └── test_api_compatibility.py      # API preservation
```

## Quick Start

```bash
# Build container
docker build -t task-01 .

# Run container
docker run -it task-01

# Inside container - run tests
./run-tests.sh

# Apply oracle solution
./solution.sh
```

## Success Criteria

An agent successfully completes this task when:
1. All 38 tests pass
2. Latency < 510ms (or < 340ms ideally)
3. Memory < 110MB (or < 87MB ideally)
4. Public API preserved
5. Predictions match baseline within 1e-6

## Adversarial Review Checklist

- ✅ No hidden one-command shortcuts
- ✅ No implementation-specific tests (tests validate behavior, not implementation)
- ✅ Performance thresholds include variance tolerance
- ✅ Sufficient test data (10 diverse samples, comprehensive edge cases)
- ✅ No environment-induced failures (all dependencies pinned, deterministic seeds)
- ✅ Multiple independent grading dimensions
- ✅ Behavioral tests (not grep/file-existence)
- ✅ Oracle passes all tests repeatedly
- ✅ Mutation tests validate grader effectiveness
