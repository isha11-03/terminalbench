# Mutation Testing

The suite is designed to kill these independent mutants:

| Mutant | Expected detection |
|---|---|
| Remove max-logit shift | overflow in extreme-logit test |
| Replace `logsumexp - target` with `-log(softmax[target])` | underflow loss test |
| Replace `math.fsum` with unstable accumulation | normalization/accuracy checks |
| Remove finite-input validation | non-finite input tests |
| Accept non-integer target | invalid-target test |
| Emit unsorted or random JSON keys | deterministic CLI test |

The baseline itself is a live mutation of the first two rows and was observed
to fail 6 of 10 tests. The oracle passed all 10 tests. No fabricated mutation
score is reported for mutants not executed independently.