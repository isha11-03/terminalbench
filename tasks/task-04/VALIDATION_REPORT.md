# Validation Report

Validation is reproducible with:

```sh
./solution.sh
./run-tests.sh
```

The suite uses only the standard library and checks an independent brute-force oracle, edge semantics, validation behavior, immutability, determinism, and a repeated baseline/candidate timing ratio. Fresh-container execution should be performed with `docker compose build --no-cache` followed by `docker compose run --rm task bash -lc './solution.sh && ./run-tests.sh'`.

This file intentionally does not contain fabricated timing or container results.
