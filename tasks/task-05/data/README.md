# Deterministic workload

The performance fixture is generated in `tests/test_kernel.py` from seed `20260922`, with 60000 rows, 24 segments, and six integer feature columns. Keeping the generator in the test makes the fixture compact while preserving a reproducible local dataset. Values are intentionally mixed-sign and bounded so exact integer arithmetic remains portable.