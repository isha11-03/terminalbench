# TASK-03: Embedding Retrieval and Ranking

## Overview

A semantic document retrieval system with subtle deficiencies in embedding normalization, filtering logic, tie-breaking, and cache invalidation. The task requires investigating the full retrieval pipeline, diagnosing issues, and implementing robust fixes.

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests (baseline - expect failures)
./run-tests.sh

# Apply fixes and verify
./solution.sh
./run-tests.sh
```

### Docker
```bash
# Build container
docker-compose build

# Run interactively
docker-compose run task-03

# Inside container
./run-tests.sh    # See failures
./solution.sh     # Apply fixes
./run-tests.sh    # Verify fixes
```

## Problem Description

Users report issues with a document retrieval system:
1. **Inconsistent retrieval quality** - relevant documents ranked poorly
2. **Non-deterministic behavior** - same query returns different orderings
3. **Filtering problems** - fewer results than expected with filters
4. **Cache inconsistencies** - stale results after configuration changes

## Structure

```
task-03/
├── instruction.md           # Task description for agent
├── solution.sh             # Oracle solution (fixes all bugs)
├── run-tests.sh            # Test runner
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container definition
├── docker-compose.yaml     # Container orchestration
│
├── data/
│   ├── corpus.json         # 20 ML documents with embeddings
│   ├── queries.json        # 10 test queries
│   └── generate_corpus.py  # Data generation script
│
├── src/
│   ├── config.py           # Configuration
│   ├── preprocessing.py    # Text preprocessing
│   ├── embeddings.py       # Embedding generation
│   ├── retrieval.py        # Core retrieval engine (has bugs)
│   └── api.py              # External API interface
│
└── tests/
    ├── test_retrieval_correctness.py  # 8 tests
    ├── test_determinism.py            # 6 tests
    ├── test_filtering.py              # 11 tests
    ├── test_edge_cases.py             # 19 tests
    ├── test_caching.py                # 6 tests
    └── test_api_compatibility.py      # 12 tests
```

## Test Suite

**Total**: 57 behavioral tests covering:
- ✅ Retrieval correctness (relevant documents rank highly)
- ✅ Deterministic behavior (reproducible results)
- ✅ Filter correctness (category/year filtering)
- ✅ Edge cases (empty queries, boundaries)
- ✅ Caching behavior (consistency and invalidation)
- ✅ API compatibility (interface contracts)

### Running Specific Tests
```bash
# Run single test file
python3 -m pytest tests/test_filtering.py -v

# Run specific test
python3 -m pytest tests/test_filtering.py::test_filtered_results_should_match_top_k -v

# Run with verbose output
python3 -m pytest tests/ -vv --tb=short
```

## Known Issues (Baseline)

The baseline implementation has several deficiencies:

1. **Embedding normalization mismatch** - Query embeddings not normalized while corpus embeddings are, causing incorrect similarity scores

2. **Filter logic order** - Top-k selection applied before filtering, returning fewer results than expected

3. **Non-deterministic tie-breaking** - No secondary sort key when scores are equal, causing inconsistent orderings

4. **Cache invalidation** - Cache not cleared when preprocessing configuration changes, returning stale results

## Expected Results

### Baseline (Before Fix)
```bash
./run-tests.sh
# Expected: ~35-40 tests pass, ~17-22 fail
# Key failures:
#   - test_filtered_results_should_match_top_k
#   - test_deterministic_ordering_with_ties (may be flaky)
#   - Several retrieval correctness tests
```

### Oracle (After Fix)
```bash
./solution.sh && ./run-tests.sh
# Expected: 57/57 tests pass
# All issues resolved, system works correctly
```

## Key Files

- **`src/retrieval.py`**: Core retrieval engine - contains most bugs
- **`src/embeddings.py`**: Embedding generation logic
- **`instruction.md`**: Problem description without revealing bugs
- **`solution.sh`**: Oracle that fixes all deficiencies

## Development

### Regenerate Data
```bash
python3 data/generate_corpus.py
```

### Run Specific Component
```bash
# Test API directly
python3 src/api.py

# Generate embeddings
python3 -c "from src.embeddings import EmbeddingGenerator; \
            gen = EmbeddingGenerator(); \
            print(gen.generate('machine learning'))"
```

## Grading Criteria

| Category | Weight | Tests |
|---|---|---|
| Retrieval correctness | 25% | 8 tests |
| Deterministic behavior | 20% | 6 tests |
| Filter correctness | 20% | 11 tests |
| Edge case handling | 15% | 19 tests |
| Caching consistency | 10% | 6 tests |
| API compatibility | 10% | 12 tests |

**Passing Threshold**: 90% (51/57 tests)

## Technical Details

### Embedding Model
Uses deterministic word-based embeddings (no downloads required):
- 64-dimensional vectors
- Fixed random seeds for reproducibility
- TF-IDF-like weighting
- Normalized to unit vectors

### Similarity Metric
Cosine similarity between query and document embeddings.

### Filtering
Supports category and year filters applied during retrieval.

### Caching
Query results cached by (query, top_k, filters) tuple.

## Documentation

- **REQUIREMENT_MATRIX.md**: Complete requirement → test → fix mapping
- **MUTATION_TESTS.md**: Mutation testing validation (90% detection rate)
- **VALIDATION_REPORT.md**: Fresh container validation results
- **QA_REPORT.md**: Comprehensive quality assurance analysis

## Dependencies

- Python 3.11+
- numpy 1.24.3
- pytest 7.4.0
- pytest-timeout 2.1.0

No network access required. No model downloads. Fully deterministic.

## Performance

- Test execution: ~0.26s
- Docker build: ~45s
- Memory usage: ~150MB

## License

Part of terminal_bench benchmark suite.
