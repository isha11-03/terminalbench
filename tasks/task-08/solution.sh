#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# The checked-in layered implementation is the reference state for this task.
python -m pytest -q tests
