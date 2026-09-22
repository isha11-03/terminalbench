# Validation Report

Status: validated locally on macOS with Python 3.12 and pytest 8.3.5.

- Baseline: `./run-tests.sh` -> `4 failed, 8 passed` (expected).
- Oracle: `./solution.sh` followed by `./run-tests.sh` -> `12 passed`.
- Oracle repeat: a second `./run-tests.sh` -> `12 passed`.
- Metadata and fixtures: local parser check passed.
- Docker fresh build: succeeded.
- Docker baseline: `4 failed, 8 passed` (expected).
- Docker oracle: `12 passed` (expected).

The oracle was installed from the checked-in reference and the baseline was
restored afterward, so the delivered source remains intentionally repairable.