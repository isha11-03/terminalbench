# TASK-04 Deliverables

- `Dockerfile`: offline Python 3.12 container.
- `task.yaml`: benchmark metadata.
- `instruction.md`: public kernel contract and workflow.
- `src/image_kernel.py`: correct but intentionally slow baseline.
- `src/image_kernel_baseline.py`: immutable benchmark baseline.
- `src/image_kernel_optimized.py`: deterministic oracle solution.
- `tests/test_kernel.py`: independent correctness, edge, API, determinism, and ratio checks.
- `data/images/`: deterministic P3 image fixtures.
- `solution.sh`: applies the reference optimization.
- `run-tests.sh`: dependency-free test entrypoint.
- `REQUIREMENT_MATRIX.md`, `MUTATION_TESTS.md`, `VALIDATION_REPORT.md`, `QA_REPORT.md`, `TASK_SUMMARY.md`, `OPTIMIZATIONS.md`, and rollout records.
