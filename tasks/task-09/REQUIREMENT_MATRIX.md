# Requirement Matrix

| ID | Requirement | Verification | Rubric dimension |
|---|---|---|---|
| R1 | Normal records produce deterministic results | `test_normal_processing_is_complete_and_ordered` | Functional correctness |
| R2 | Identical duplicate IDs are one logical item | `test_identical_duplicate_input_is_processed_once` | Duplicate handling |
| R3 | Conflicting duplicate payloads are rejected before mutation | `test_conflicting_duplicate_is_rejected_before_mutation` | Input integrity |
| R4 | Failed work is retryable and completed progress is retained | `test_retry_preserves_progress_and_increments_only_failed_item` | Retry/recovery |
| R5 | Repeated successful runs are idempotent | `test_rerun_is_idempotent` | Idempotency |
| R6 | Missing output can be repaired from completed state | `test_completed_state_repairs_missing_output_without_reprocessing` | Persistence correctness |
| R7 | Stale running work resumes after restart | `test_restart_reprocesses_stale_running_item` | Restart behavior |
| R8 | Malformed state is rejected clearly | `test_malformed_persistence_is_rejected` | State consistency |
| R9 | Public recovery/reset API remains compatible | `test_recover_and_reset_public_api` | API compatibility |
| R10 | Failure persistence remains valid JSON | `test_failure_leaves_valid_json_persistence` | Partial failure safety |
| R11 | Results and test runs are repeatable | repeated `./run-tests.sh` and oracle checks | Determinism |
