# Requirement Matrix

| ID | Requirement | Test evidence |
|---|---|---|
| R1 | Solve deterministic SPD systems | `test_solution_and_residual` |
| R2 | Meet relative residual tolerance | `test_solution_and_residual`, `test_relative_tolerance_and_initial_guess` |
| R3 | Keep CSR operations sparse | `test_sparse_matvec_does_not_call_dense_conversion` |
| R4 | Respect `x0` and iteration budget | `test_relative_tolerance_and_initial_guess`, `test_zero_rhs_and_budget_reporting` |
| R5 | Handle zero RHS and invalid controls | `test_zero_rhs_and_budget_reporting`, `test_invalid_controls` |
| R6 | Preserve dimensions, loader, and deterministic behavior | `test_invalid_dimensions_and_loader`, `test_deterministic_result` |