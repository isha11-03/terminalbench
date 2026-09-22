# TASK-08: Order Service Architecture Refactor

This task asks an agent to separate a coupled order application into domain,
service, persistence, configuration, composition, API, and CLI layers while
preserving its public behavior. The initial `legacy_order_app.py` is the
baseline coupling specimen; `order_app/` is the refactored application surface.

The tests cover functional behavior, durable configuration, injected
repositories, errors, CLI output, and exact dependency direction. The pure
functions in `src/reference_solution.py` provide an independent behavioral
oracle for order creation and cancellation.
