#!/bin/bash
# Oracle solution script
# Applies the optimized implementation

set -e

echo "Applying optimized inference pipeline..."

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Backup the original implementation
if [ ! -f "src/inference_pipeline.py.backup" ]; then
    cp src/inference_pipeline.py src/inference_pipeline.py.backup
    echo "Backed up original implementation"
fi

# Replace with optimized version
cp src/inference_pipeline_optimized.py src/inference_pipeline.py

echo "Optimization applied successfully"
echo ""
echo "Key optimizations:"
echo "1. Removed unnecessary string copies in preprocessing"
echo "2. Used regex for efficient character cleaning"
echo "3. Optimized stopword removal with list comprehension"
echo "4. Eliminated redundant data copying in feature extraction"
echo "5. Kept sparse matrix format (avoid dense conversion)"
echo "6. Batch predict/predict_proba to avoid repeated model calls"
echo "7. Removed redundant probability normalization"
echo "8. Removed ineffective result caching"
echo ""
echo "Running tests to verify correctness..."
./run-tests.sh
