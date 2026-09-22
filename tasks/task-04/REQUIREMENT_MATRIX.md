# Requirement Matrix

| ID | Requirement | Evidence |
|---|---|---|
| R1 | RGB box blur keeps public signature | `tests/test_kernel.py::test_validation_and_shape` |
| R2 | Clamp-to-edge and exact floor arithmetic | independent `oracle` plus boundary/radius cases |
| R3 | Empty, zero-radius, singleton, rectangular, and oversized-radius inputs | `test_empty_zero_radius_and_input_immutability`, normal/boundary matrix |
| R4 | Negative radius and ragged rows fail with `ValueError` | `test_validation_and_shape` |
| R5 | Input is not mutated; output is fresh | immutability assertions |
| R6 | Repeated calls are deterministic | `test_deterministic_repeated_call` |
| R7 | Optimized implementation agrees with an independent oracle | `test_normal_and_boundary_values_match_independent_oracle` |
| R8 | Measurable improvement with container-tolerant ratio | `test_optimized_kernel_beats_baseline_ratio` |
| R9 | No network or third-party runtime dependency | empty `requirements.txt`, offline Dockerfile |
| R10 | Mutation resistance covers output, boundary, numerical, regression, and performance defects | `MUTATION_TESTS.md` |
