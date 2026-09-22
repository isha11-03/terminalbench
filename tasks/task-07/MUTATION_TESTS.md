# Mutation Testing

| Mutant | Intended killed by |
|---|---|
| Call `to_dense()` from `matvec` | sparse conversion test |
| Stop on absolute `tol` only | scaled relative-tolerance case |
| Always initialize `x` to zero | initial-guess case |
| Divide by zero for zero RHS | zero-RHS case |
| Ignore `max_iter` or claim convergence at budget | budget-reporting case |
| Permit zero, NaN, or fractional controls | invalid-controls case |
| Add nondeterministic perturbation | deterministic-result case |

Observed validation: the baseline run produced `4 failed, 8 passed`; the
failures exercise dense conversion, residual/convergence behavior, and initial
guess handling. The oracle run produced `12 passed` twice. The suite detects
the listed baseline mutations; no additional unexecuted mutation score is
claimed.