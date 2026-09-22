#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
cp src/memory_kernel_optimized.py src/memory_kernel.py
python -m py_compile src/memory_kernel.py
