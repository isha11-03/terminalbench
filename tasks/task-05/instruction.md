# TASK-05: Memory-bound segmented feature reduction

Optimize `src/memory_kernel.py` without changing its public API or exact results.

`reduce_records(records, segment_count)` consumes a sequence of fixed-width rows. Each row is a 7-tuple: `(segment, feature_0, feature_1, feature_2, feature_3, feature_4, feature_5)`. It returns one tuple per segment: `(count, sum_0, sum_1, sum_2, sum_3, sum_4, sum_5, min_total, max_total)`, where `total` is the sum of the six feature values for one row. Empty segments use zero for every field, including the extrema.

The supplied implementation is correct but intentionally creates row copies and intermediate feature collections, performs repeated per-row mapping work, and uses an indirect dictionary of accumulator objects. Investigate the data movement and locality before changing it. Improve throughput or memory behavior using only the Python standard library; multiple optimization strategies are valid and the tests do not inspect source text.

## Contract

- Preserve the callable signature and tuple output shape.
- Accept empty input and `segment_count == 0` only when the input is empty.
- Support one row, repeated segments, negative feature values, and segments with no rows.
- Reject a negative segment count, a non-integer segment count, ragged rows, out-of-range segment ids, non-integer fields, and boolean values with `ValueError`.
- Do not mutate the input or any input row. Results must be deterministic and use exact integer arithmetic.
- Do not add third-party runtime dependencies or use network access.

## Investigation and validation

Read both the baseline and the surrounding tests, establish a baseline timing, and explain the chosen optimization in your work. Run the supplied tests after applying your implementation. The performance check uses repeated timings on a deterministic wide-record workload and includes a margin for ordinary container noise; avoid one-shot microbenchmarks.
