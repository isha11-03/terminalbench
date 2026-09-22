# TASK-07: Sparse Conjugate Gradient

This benchmark repairs a small CSR matrix and Conjugate Gradient API. The
baseline contains interacting defects around dense conversion, relative
residual scaling, initial guesses, zero right-hand sides, and iteration
reporting. Tests assert mathematical invariants and public behavior rather
than a particular loop structure.

The oracle is `src/reference_solution.py`; `solution.sh` installs it and runs
the same tests. No network or third-party numerical library is required.
