# Requirement Matrix

| ID | Requirement | Instruction | Behavioral test | Rubric/oracle evidence |
|---|---|---|---|---|
| R1 | Solve deterministic SPD systems accurately | API and SPD paragraphs | `test_solution_and_residual` | Reference CG result and residual |
| R2 | Use relative residual rule | relative stopping paragraph | `test_solution_and_residual`, `test_relative_tolerance_and_initial_guess` | Reference threshold `tol * max(1, ||b||)` |
| R3 | Keep CSR operations sparse | sparse matvec paragraph | `test_sparse_matvec_does_not_call_dense_conversion`, `test_solver_does_not_call_dense_conversion` | Reference `matvec` traverses CSR entries |
| R4 | Respect `x0` and iteration budget | initialization and budget paragraphs | `test_relative_tolerance_and_initial_guess`, `test_zero_rhs_and_budget_reporting` | Reference initializes from `x0` and reports exhaustion |
| R5 | Handle zero RHS immediately | zero RHS paragraph | `test_zero_rhs_and_budget_reporting` | Reference returns zero solution at iteration 0 |
| R6 | Reject invalid controls | validation paragraph | `test_invalid_controls` | Reference validates finite positive tolerance and integer budget |
| R7 | Reject incompatible and non-square dimensions | validation paragraph | `test_invalid_dimensions_and_loader` | Reference validates matrix/vector/guess dimensions |
| R8 | Load supplied CSR JSON fixtures | loader paragraph | `test_invalid_dimensions_and_loader` | Reference `load_matrix` parses local JSON |
| R9 | Preserve deterministic behavior | deterministic paragraph | `test_deterministic_result` | Repeated reference calls are equal |