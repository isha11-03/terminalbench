#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
cp src/image_kernel_optimized.py src/image_kernel.py
python -m py_compile src/image_kernel.py
