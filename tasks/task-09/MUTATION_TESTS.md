# Mutation Test Plan

The acceptance suite is designed to kill these behavioral mutations:

| Mutation | Expected detector |
|---|---|
| Append outputs instead of replacing by logical ID | normal, duplicate, and idempotency tests |
| Process every duplicate input line | duplicate and idempotency tests |
| Persist only at normal completion | retry and failure-persistence tests |
| Mark failed work completed | retry test |
| Reset all attempts after restart | retry and restart tests |
| Ignore completed state when output is missing | completed-state repair test |
| Accept conflicting duplicate payloads | conflicting-duplicate test |
| Leave `running` records permanently skipped | restart test |
| Write malformed/non-object state | malformed-state and failure-persistence tests |
| Change `recover` or `reset` signatures/semantics | public API test |

These are behavioral mutations, not source-pattern checks. A fresh-container run and repeated oracle runs are required before claiming completion.
