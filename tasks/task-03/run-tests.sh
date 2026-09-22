#!/bin/bash
set -e

echo "Running test suite for embedding retrieval system..."
echo

# Run tests with pytest
python -m pytest tests/ -v --tb=short --timeout=30

echo
echo "Test suite complete."
