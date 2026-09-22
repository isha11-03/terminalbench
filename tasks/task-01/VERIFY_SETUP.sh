#!/bin/bash
# Verification script to check task setup completeness
# Run this before deployment to ensure everything is ready

set -e

echo "=================================="
echo "Task-01 Setup Verification"
echo "=================================="
echo ""

ERRORS=0
WARNINGS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo "✓ $1"
    else
        echo "✗ MISSING: $1"
        ((ERRORS++))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo "✓ $1/"
    else
        echo "✗ MISSING: $1/"
        ((ERRORS++))
    fi
}

# Function to check file is not empty
check_not_empty() {
    if [ -s "$1" ]; then
        echo "✓ $1 (not empty)"
    else
        echo "⚠ WARNING: $1 is empty"
        ((WARNINGS++))
    fi
}

# Function to count words in file
check_word_count() {
    local file=$1
    local max=$2
    if [ -f "$file" ]; then
        local count=$(wc -w < "$file")
        if [ "$count" -le "$max" ]; then
            echo "✓ $file word count: $count/$max"
        else
            echo "✗ ERROR: $file has $count words, exceeds $max limit"
            ((ERRORS++))
        fi
    fi
}

echo "Checking Core Files..."
check_file "Dockerfile"
check_file "requirements.txt"
check_file "task.yaml"
check_file "instruction.md"
check_file "solution.sh"
check_file "run-tests.sh"
echo ""

echo "Checking Documentation..."
check_file "README.md"
check_file "REQUIREMENT_MATRIX.md"
check_file "MUTATION_TESTS.md"
check_file "VALIDATION_REPORT.md"
check_file "QA_REPORT.md"
check_file "ROLLOUT_TEMPLATE.md"
check_file "TASK_SUMMARY.md"
echo ""

echo "Checking Source Code..."
check_dir "src"
check_file "src/__init__.py"
check_file "src/inference_pipeline.py"
check_file "src/inference_pipeline_optimized.py"
echo ""

echo "Checking Data & Models..."
check_dir "data"
check_file "data/__init__.py"
check_file "data/generate_model.py"
echo ""

echo "Checking Tests..."
check_dir "tests"
check_file "tests/__init__.py"
check_file "tests/test_correctness.py"
check_file "tests/test_edge_cases.py"
check_file "tests/test_performance.py"
check_file "tests/test_api_compatibility.py"
echo ""

echo "Checking File Contents..."
check_not_empty "Dockerfile"
check_not_empty "requirements.txt"
check_not_empty "instruction.md"
check_not_empty "src/inference_pipeline.py"
check_not_empty "src/inference_pipeline_optimized.py"
echo ""

echo "Checking Word Count..."
check_word_count "instruction.md" 600
echo ""

echo "Checking Script Permissions..."
if [ -x "run-tests.sh" ]; then
    echo "✓ run-tests.sh is executable"
else
    echo "⚠ WARNING: run-tests.sh is not executable"
    ((WARNINGS++))
fi

if [ -x "solution.sh" ]; then
    echo "✓ solution.sh is executable"
else
    echo "⚠ WARNING: solution.sh is not executable"
    ((WARNINGS++))
fi
echo ""

echo "Checking Python Syntax..."
python -m py_compile src/inference_pipeline.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ src/inference_pipeline.py syntax OK"
else
    echo "✗ ERROR: src/inference_pipeline.py has syntax errors"
    ((ERRORS++))
fi

python -m py_compile src/inference_pipeline_optimized.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ src/inference_pipeline_optimized.py syntax OK"
else
    echo "✗ ERROR: src/inference_pipeline_optimized.py has syntax errors"
    ((ERRORS++))
fi

python -m py_compile data/generate_model.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ data/generate_model.py syntax OK"
else
    echo "✗ ERROR: data/generate_model.py has syntax errors"
    ((ERRORS++))
fi
echo ""

echo "=================================="
echo "Verification Summary"
echo "=================================="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo "✓ ALL CHECKS PASSED"
        echo "Task-01 is ready for deployment!"
        exit 0
    else
        echo "⚠ PASSED WITH WARNINGS"
        echo "Task-01 is usable but review warnings above"
        exit 0
    fi
else
    echo "✗ VERIFICATION FAILED"
    echo "Fix errors above before deployment"
    exit 1
fi
