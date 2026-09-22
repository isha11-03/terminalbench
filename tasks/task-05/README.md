# TASK-05: Memory-Bound Segmented Feature Reduction

This is a self-contained benchmark for optimizing a wide-record, segmented numerical reduction. The baseline and optimized implementations expose the same exact-integer API; `solution.sh` installs the optimized candidate and `run-tests.sh` runs correctness, boundary, determinism, resource, and repeated performance checks.

```sh
./solution.sh
./run-tests.sh
```

Only Python 3.12 and pytest are required. The workload is generated from a checked-in seed and does not require network access.

Do not pad the task with unrelated subtasks.
