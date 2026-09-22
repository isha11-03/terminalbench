# Requirement Matrix

| ID | Requirement | Prompt | Test / oracle | Rubric dimension |
|---|---|---|---|---|
| R1 | Preserve `reduce_records(records, segment_count)` and 9-field output tuples | Contract | `test_normal_and_boundary_values_match_independent_oracle` | Interface |
| R2 | Exact count, column sums, and min/max row totals | Output definition | Independent `oracle` and large-value test | Numerical correctness |
| R3 | Empty input, zero segments, singleton, sparse segments, mixed signs | Contract | `test_empty_zero_segments_and_single_row_cases` | Boundary behavior |
| R4 | Reject malformed rows, bad counts, out-of-range ids, non-integers, booleans | Contract | parametrized validation tests | Input validation |
| R5 | Never mutate input; deterministic repeat calls | Contract | immutability and determinism tests | Compatibility |
| R6 | Candidate improves throughput over allocation-heavy baseline | Performance requirement | three paired timings, median ratio >= 1.25 | Throughput |
| R7 | No network or third-party runtime dependency beyond pytest harness | Constraints | offline Dockerfile and requirements | Resource/environment |
| R8 | Mutation coverage for each grading dimension | QA requirement | `MUTATION_TESTS.md` execution plan | Adversarial QA |
| R9 | Fresh-container reproducibility and honest rollout status | Lifecycle | `VALIDATION_REPORT.md`, `ROLLOUT_RECORD.md` | Release quality |