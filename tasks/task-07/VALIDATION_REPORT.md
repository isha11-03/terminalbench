# Validation Report

Status: validated locally on macOS with Python 3.12 and pytest 8.3.5.

- Baseline: `bash run-tests.sh` -> `5 failed, 6 passed` (expected).
- Oracle: `bash solution.sh` -> `11 passed`.
- Structure: `python scripts/validate_structure.py` -> `Structure OK`.

The oracle was installed from the checked-in reference and the baseline was
restored afterward, so the delivered source remains intentionally repairable.