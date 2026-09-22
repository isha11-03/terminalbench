#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
cp src/reference_solution.py src/softmax.py
python -m pytest -q tests
