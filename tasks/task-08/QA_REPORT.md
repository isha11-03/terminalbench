# QA Report

The task has one focused engineering objective: remove architectural coupling
from the order application without changing its public behavior. Coverage
spans normal orders, decimal edge cases, invalid input, missing records,
repeated cancellation, environment-selected persistence, CLI output, fake
repositories, and dependency direction.

Known risk: `legacy_order_app.py` is retained as a baseline specimen and is not
used by the refactored public package. The benchmark instruction makes the
required migration explicit. Docker validation must be rerun whenever the
runtime image or dependency pin changes.
