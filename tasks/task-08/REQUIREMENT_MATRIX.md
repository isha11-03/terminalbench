# Requirement Matrix

| ID | Requirement | Evidence |
|---|---|---|
| R1 | Public create/get API persists orders | `test_public_api_and_persistence` |
| R2 | Decimal totals normalize to two places | `test_public_api_and_persistence` |
| R3 | Cancellation is idempotent and missing orders are explicit | `test_cancel_is_idempotent_and_missing_is_clear` |
| R4 | Invalid inputs are rejected | `test_invalid_orders` |
| R5 | Service depends on an injected repository port | `test_fake_repository_is_enough_for_service` |
| R6 | Core layers do not import infrastructure concerns | `test_dependency_direction_has_no_infrastructure_imports_in_core` |
| R7 | Environment configuration and CLI remain compatible | `test_cli_entrypoint`, `test_public_api_and_persistence` |
| R8 | Results are deterministic and standard-library-only | full suite and container build |
