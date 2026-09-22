# Mutation Test Notes

The mutation plan targets independent grading dimensions:

| Mutation | Expected detection |
|---|---|
| Remove `Decimal` quantization | persistence/API total assertions fail |
| Save without status update | persistence and cancellation assertions fail |
| Make cancellation non-idempotent | idempotence assertion fails |
| Ignore `ORDER_DATA_FILE` | temporary-path persistence and CLI tests fail |
| Replace repository injection with a concrete JSON repository | fake-repository test or import-direction review fails |
| Add `json` import to service | dependency-direction test fails |
| Return `None` for missing orders | missing-order error test fails |
| Make CLI output nondeterministic | exact CLI output assertion fails |

Each mutation is local and should produce a non-zero test result; no mutation
results are claimed here until they are executed in a clean environment.
