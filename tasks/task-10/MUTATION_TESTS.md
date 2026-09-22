# Mutation Tests

The suite is intended to kill these mutations:

| Mutation | Detector |
|---|---|
| Drop or duplicate valid propagation | Stream ordered scoreboard |
| Ignore output backpressure | Stream stall schedule and stable ordering |
| Make stage one non-elastic | Stream accepted/received counts |
| Truncate multiply to input width | Signed boundary and generated vectors |
| Treat operands as unsigned | Negative operand vectors |
| Add one or remove one pipeline stage | Exact latency test |
| Retain valid across reset | Reset portion of latency bench |
| Gate throughput to every other cycle | Sustained stream count and completion |

The baseline is expected to fail behavioral tests. Mutation results are recorded only for mutations actually executed; no unrun rollout scores are claimed.
