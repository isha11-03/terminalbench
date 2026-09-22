# TASK-09: Stateful Data-Processing Reliability

Repair a deterministic local JSON-backed batch pipeline under retries, duplicate input, partial progress, failed work, and restart recovery. The baseline in `src/job.py` is intentionally incomplete; `src/reference_solution.py` is the independent oracle used by `solution.sh`.

The acceptance suite checks observable outputs, durable state transitions, idempotent reruns, duplicate semantics, recovery, malformed persistence, and public API compatibility. It does not require an external database, network, or runtime dependency beyond Python and pytest.
