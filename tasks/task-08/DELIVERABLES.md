# TASK-08 Deliverables

- Problem design: coupled order application refactor with compatibility constraints.
- Environment: Dockerfile, docker-compose.yaml, requirements.txt.
- Baseline: `src/legacy_order_app.py` with global configuration and persistence.
- Target: `src/order_app/` layered domain, ports, service, infrastructure, composition, API, and CLI.
- Deterministic data: `data/orders.json`.
- Oracle: `src/reference_solution.py` independently models domain outcomes.
- Tests: ten behavioral and structural tests in `tests/test_order_app.py`.
- Validation: run-tests, mutation notes, fresh-container validation, QA, and rollout records.
