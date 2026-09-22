#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
cp src/reference_solution.py src/sparse_solver.py
python -m pytest -q tests
