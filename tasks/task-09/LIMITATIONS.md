# Limitations

This task models one local process and deterministic JSON persistence. It does not claim distributed multi-process locking, filesystem durability across hardware failure, schema migration, or unbounded-file performance. The failure injector is a deterministic test seam; real operating-system crashes are approximated by persisted `running` state and rerun behavior.
