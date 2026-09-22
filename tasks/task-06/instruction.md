# Task

## Context
You are working in a local engineering repository containing a deliberately constrained implementation.

## Objective
Repair `src/softmax.py` so its existing `logsumexp`, `softmax`,
`cross_entropy`, and JSON CLI remain API-compatible and are mathematically
correct and numerically stable for finite floating-point logits.

## Constraints
- Work only with files and dependencies available in the container.
- Do not rely on network access.
- Preserve existing public interfaces unless the task explicitly requires a change.
- Keep the result deterministic and reproducible.

## Acceptance criteria
1. Probabilities are finite, non-negative, normalized to one, and invariant to
	adding a constant to every logit.
2. `logsumexp` is accurate for very large positive and negative finite logits.
3. Cross-entropy remains finite and accurate when the target probability would
	underflow; use the mathematically equivalent log-domain expression.
4. Empty, non-finite, and invalid-target inputs raise the documented built-in
	exceptions without nondeterministic behavior.
5. The JSON CLI output keeps the existing keys and is deterministic.
6. The implementation should be linear in the number of logits and use only
	O(n) temporary storage.

## Deliverable
Leave the repository in the final working state and verify it before finishing.

Do not assume that the existing implementation, tests, or documentation are complete. Inspect the repository and determine what must change.
