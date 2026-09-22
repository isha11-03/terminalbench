# Final QA Report

## Passed

- Ordinary probabilities and loss are checked against deterministic values.
- Extreme positive, extreme negative, and wide-range logits remain finite.
- Adding a constant preserves probabilities.
- Cross-entropy avoids probability underflow.
- Invalid numeric inputs and targets are rejected deterministically.
- CLI output is API-compatible and byte-for-byte deterministic.
- The complete ten-test local suite passes after `bash solution.sh`.

## Open verification

Docker fresh-container execution should be run in an environment with Docker
available. The repository does not claim a result that has not been observed.