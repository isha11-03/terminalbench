#!/bin/bash
# Test execution script
# Runs all test suites and reports results

set -e

echo "==================================="
echo "ML Inference Pipeline - Test Suite"
echo "==================================="
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Generate model if it doesn't exist
if [ ! -d "data/model" ] || [ ! -f "data/model/model.pkl" ]; then
    echo "Generating model and test data..."
    python data/generate_model.py
    echo ""
fi

# Run pytest with verbose output
echo "Running test suite..."
echo ""

# Run tests with detailed output
python -m pytest tests/ -v --tb=short \
    --ignore=tests/test_placeholder.py \
    -W ignore::DeprecationWarning

exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
    echo "==================================="
    echo "All tests passed successfully!"
    echo "==================================="
else
    echo "==================================="
    echo "Some tests failed (exit code: $exit_code)"
    echo "==================================="
fi

exit $exit_code
