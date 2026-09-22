# Mutation Results

Construction-time verification performed the following live checks:

| Check | Result |
|---|---|
| Defective baseline stream test | Failed with invalid extra output handshakes |
| Defective baseline latency test | Failed latency/data assertion |
| Independent reference stream test | Passed in fresh Docker image |
| Reference latency test | Available in full suite; baseline failure is intentional |

A complete automated mutation campaign was not run during construction, so no fabricated kill-rate is reported.
