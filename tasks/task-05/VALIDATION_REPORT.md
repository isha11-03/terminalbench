# Validation Report

## Local

```sh
bash solution.sh && bash run-tests.sh
```

Result: 8 tests passed in 0.76 seconds, including correctness, boundary, validation, immutability, determinism, and the repeated baseline/candidate throughput ratio.

## Fresh container

Run:

```sh
docker compose build --no-cache
docker compose run --rm task bash -lc 'bash solution.sh && bash run-tests.sh'
```

Result: clean Docker Compose build completed and the container run passed 8 tests in 0.73 seconds. The build resolved the Python base image and installed the pytest harness successfully.