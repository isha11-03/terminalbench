# Terminal-Bench-Style Starter Pack

A modifiable scaffold for a 10-task benchmark:
- 3 ML/AI
- 2 kernel optimization
- 2 scientific computing
- 2 software engineering
- 1 RTL

Each task is intended to become one coherent, deterministic, self-contained engineering problem requiring exploration, implementation, debugging and verification.

## Per-task contract

```text
task-NN/
├── Dockerfile
├── docker-compose.yaml 
├── task.yaml
├── instruction.md        # <= 600 words
├── solution.sh           # deterministic oracle
├── run-tests.sh
├── tests/
├── src/
└── data/
```

## Workflow

1. Choose one deep problem.
2. Build a realistic local baseline/failure mode.
3. Define observable acceptance criteria.
4. Write independent behavioral tests.
5. Implement and validate the oracle.
6. Mutation-test the grader.
7. Rebuild from a fresh container.
8. Run five model rollouts.
9. Analyze scores, steps and failures.
10. Perform RCA and iterate.

Difficulty must come from engineering reasoning and iteration, not ambiguity, network access, obscure one-command tricks, or artificial task chaining.
