# Oracle

`src/reference_solution.sv` is an independently written elastic two-register pipeline. It uses explicit signed extension before full-width multiplication and computes ready from both pipeline occupancy and downstream readiness.

The oracle is exercised by the same behavioral benches through `tests/test_placeholder.py`. The grader does not compare source text or depend on oracle output files; it checks simulator behavior. Construction validation ran the oracle in a fresh Docker image with all three tests passing.
