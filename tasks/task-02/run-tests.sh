#!/bin/bash
set -e

# Generate data if it doesn't exist
if [ ! -f demand_data.csv ]; then
    echo "Generating demand data..."
    python3 data/generate_data.py
fi

# Run pytest with verbose output
echo "Running test suite..."
python3 -m pytest tests/ -v --tb=short --timeout=60

echo ""
echo "All tests passed!"
