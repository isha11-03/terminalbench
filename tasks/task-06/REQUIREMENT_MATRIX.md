# Requirement Matrix

| ID | Requirement | Prompt | Test | Rubric/oracle |
|---|---|---|---|---|
| R1 | Ordinary softmax is mathematically correct | Acceptance 1 | `test_ordinary_probabilities_and_loss` | exact reference values within tolerance |
| R2 | Stable for positive/negative extreme logits | Acceptance 1-2 | `test_extreme_logits_are_finite_and_shift_invariant` | finite, normalized, shift invariant |
| R3 | Stable log-domain cross-entropy | Acceptance 3 | `test_cross_entropy_uses_logsumexp_without_probability_underflow` | loss near 1000 |
| R4 | Reject empty and non-finite values | Acceptance 4 | `test_rejects_empty_or_nonfinite_values` | `ValueError` |
| R5 | Reject invalid targets | Acceptance 4 | `test_rejects_invalid_targets` | `TypeError`/`IndexError` |
| R6 | CLI compatibility and determinism | Acceptance 5 | `test_cli_is_deterministic_and_matches_api` | stable JSON keys and bytes |
| R7 | Deterministic local cases | Deterministic data | `test_deterministic_data_cases_are_covered` | fixed case order |
| R8 | Linear work and O(n) storage | Acceptance 6 | code review and bounded input design | two-pass stable algorithm |