# Mutation Testing

Mutation targets and expected independent-test failures:

| Mutation | Expected detector |
|---|---|
| Return the input unchanged | normal correctness and radius tests |
| Use a clipped-area divisor at boundaries | independent oracle on singleton/oversized-radius case |
| Remove left or right clamp contribution | boundary oracle cases |
| Change one channel divisor or add one to the result | exact numerical oracle |
| Change `radius == 0` to blur | zero-radius and API tests |
| Allow ragged rows | validation test |
| Reuse the input rows | immutability test |
| Add a random tie-breaker or mutable cache | determinism test |
| Replace optimized body with baseline | performance ratio test |

Mutation evidence is recorded only after executing the mutation commands; no unexecuted rollout claim is made here.
