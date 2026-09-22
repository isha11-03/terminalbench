# TASK-05 Deliverables

- `Dockerfile`, `docker-compose.yaml`, `requirements.txt`: local Python 3.12 test environment.
- `task.yaml`, `instruction.md`, `README.md`: task metadata and solver contract.
- `src/memory_kernel.py`: installed candidate entry point.
- `src/memory_kernel_baseline.py`: correct allocation-heavy comparison implementation.
- `src/memory_kernel_optimized.py`: deterministic reference optimization used by `solution.sh`.
- `tests/test_kernel.py`: independent oracle, contract, boundary, mutation-sensitive, and repeated performance tests.
- `data/README.md`: deterministic workload provenance.
- `solution.sh`, `run-tests.sh`: reproducible setup and test entry points.
- `REQUIREMENT_MATRIX.md`, `MUTATION_TESTS.md`, `OPTIMIZATIONS.md`, `VALIDATION_REPORT.md`, `QA_REPORT.md`, `LIMITATIONS.md`, `TASK_SUMMARY.md`, `ROLLOUT_RECORD.md`: lifecycle evidence.