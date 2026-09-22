# TASK-07: Sparse Conjugate-Gradient Solver

Repair `src/sparse_solver.py`, preserving its public API. `SparseMatrix` is a
CSR matrix with zero-based `row_ptr`, `col_idx`, and `values`; `load_matrix`
loads the supplied JSON fixture. `solve_cg(matrix, b, tol=1e-8, max_iter=None,
x0=None)` returns a dictionary with `x`, `iterations`, `residual_norm`, and
`converged`.

The solver must use sparse matrix-vector products (do not convert the matrix
to dense), solve symmetric positive-definite systems, and be deterministic.
Use the relative stopping rule `||b - A x|| <= tol * max(1, ||b||)`. Respect a
valid `x0`, default `max_iter` to the number of rows, and report
`converged=False` rather than claiming success when the iteration budget is
exhausted. A zero right-hand side should return the zero solution immediately.
Reject invalid tolerances, incompatible dimensions, and non-positive iteration
budgets with `ValueError`; reject a non-square matrix with `ValueError`.

Use only the local files and standard library. Run `./run-tests.sh` after your
changes. Do not change the tests or the reference solution.
