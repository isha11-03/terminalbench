# TASK-06: Numerically Stable Softmax

This benchmark asks an agent to repair a small scientific-computing API for
`logsumexp`, softmax probabilities, and multiclass cross-entropy. The supplied
baseline uses direct exponentiation and is deliberately unstable for large or
very negative logits. The public functions and JSON CLI must remain compatible.

The reference solution shifts by the maximum logit, uses `math.fsum` for the
normalization, and computes cross-entropy as `logsumexp(logits) - logits[target]`
so it does not take a logarithm of a probability that has already underflowed.

Run `./solution.sh` to install the oracle implementation and run the complete
test suite. `./run-tests.sh` runs the tests without changing the implementation.
