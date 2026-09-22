#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
cp src/reference_solution.sv src/stream_accel.sv
python -m pytest -q tests
