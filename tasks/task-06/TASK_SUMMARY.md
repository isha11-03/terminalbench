# Task Summary

TASK-06 is a single numerical-method repair problem. A naive implementation
computes `exp(logit)` directly, which overflows for large positive logits and
loses information for large negative logits. The repaired method subtracts the
maximum before exponentiation and evaluates cross-entropy directly in the
log-domain. The public function names, return types, exceptions, and CLI JSON
keys are preserved.