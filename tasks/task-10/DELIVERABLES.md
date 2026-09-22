# Deliverables

- `Dockerfile`, `docker-compose.yaml`, `requirements.txt`: isolated Python/Icarus environment.
- `src/stream_accel.sv`: deliberately defective two-stage baseline.
- `src/reference_solution.sv`: independent passing oracle.
- `tests/tb_stream.sv`: sustained traffic, signed boundaries, stalls, and scoreboarding.
- `tests/tb_latency.sv`: reset and exact two-cycle latency checks.
- `tests/test_placeholder.py`: pytest wrapper for simulator behavior.
- `instruction.md`, `run-tests.sh`, `solution.sh`, `task.yaml`: task interface.
- Evidence documents: requirement matrix, mutation plan/results, validation, rollout record, QA, and limitations.
