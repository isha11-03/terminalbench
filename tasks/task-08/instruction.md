# TASK-08: Order Service Architecture Refactor

Refactor this repository's order application while preserving its observable behavior and public compatibility.

The baseline implementation is in `src/legacy_order_app.py`: it mixes domain validation, process-global configuration, JSON persistence, and API behavior in one module. The repository also contains the intended public API names (`create_order`, `get_order`, `cancel_order`, and `reset`) and a CLI contract. Treat existing behavior as the contract, including two-decimal monetary normalization, durable JSON storage, the `ORDER_DATA_FILE` environment variable, missing-order errors, cancellation rules, idempotent cancellation, and deterministic CLI output.

The final design must make dependency direction explicit: domain and service logic must not import JSON, environment, or concrete persistence code; persistence must be replaceable in service tests; configuration and infrastructure must be composed at an application boundary; and the public API must remain usable without callers constructing infrastructure objects. Preserve standard-library-only runtime behavior and deterministic results.

Use the supplied tests as executable acceptance criteria, but inspect the complete repository and reason about compatibility before changing code. Do not modify tests or the independent reference oracle. Run `./run-tests.sh` from this directory before finishing.

Acceptance requires:
- all functional, edge-case, persistence, CLI, and compatibility tests pass;
- the service works with an injected repository implementation;
- dependency-direction checks pass without relying on prescribed filenames beyond public entry points;
- configuration remains environment-driven and deterministic;
- the solution uses no network access or new runtime dependencies.

