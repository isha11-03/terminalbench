# Validation Report

Validation commands for this task:

```text
./run-tests.sh                 # baseline should expose reliability failures
./solution.sh                  # install oracle and run all tests
./run-tests.sh                 # repeat after oracle installation
```

Observed results:

- Baseline: 7 passed, 4 failed, exposing the intended reliability defects.
- Host oracle: 10 passed; repeated host run: 10 passed.
- Fresh Docker Compose baseline: 7 passed, 4 failed.
- Fresh Docker Compose oracle: 10 passed.

No rollout result is fabricated in this document. Benchmark rollout scoring remains a harness responsibility.
