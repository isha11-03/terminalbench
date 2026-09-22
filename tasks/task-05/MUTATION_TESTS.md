# Mutation Testing Plan

The following mutations must be applied one at a time to `src/memory_kernel.py`; each is expected to make the supplied suite fail. Results are not claimed here unless the mutation is actually executed.

| Mutation | Expected detector |
|---|---|
| Drop one feature accumulator | Independent oracle and large-value test |
| Use a clipped or wrong extrema value for empty segments | Boundary oracle |
| Change one sum or total comparison | Exact numerical oracle |
| Return the input or reuse an input row | Immutability and output-shape tests |
| Accept booleans or ragged rows | Validation tests |
| Ignore segment ids or merge segments | Sparse-segment oracle |
| Add nondeterministic ordering/state | Repeated-call determinism test |
| Replace candidate with baseline | Repeated performance ratio |

The baseline is separately checked against the independent oracle so a defective comparator is not mistaken for a candidate defect.