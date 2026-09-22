# TASK-06 Deliverables

- Problem design: stable log-sum-exp, softmax, and cross-entropy repair.
- Environment: `Dockerfile`, `docker-compose.yaml`, and pinned `requirements.txt`.
- Baseline: intentionally unstable `src/softmax.py`.
- Oracle: `src/reference_solution.py`, installed by `solution.sh`.
- Deterministic data: `data/cases.json`.
- Tests: `tests/test_softmax.py`, run by `run-tests.sh`.
- Lifecycle records: `REQUIREMENT_MATRIX.md`, `MUTATION_TESTS.md`,
  `VALIDATION_REPORT.md`, `ROLLOUT_RECORD.md`, `QA_REPORT.md`, and
  `LIMITATIONS.md`.