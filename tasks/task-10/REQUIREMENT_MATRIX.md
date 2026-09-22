# Requirement Matrix

| Requirement | Test evidence | Rubric/oracle |
|---|---|---|
| Correct signed arithmetic | `tb_stream` boundary and generated vectors | Oracle stream pass |
| Two-cycle latency | `tb_latency` | Accepted/output cycle delta is 2 |
| Sustained throughput | 24 transactions with one-cycle source | 24 accepted and received |
| Valid/ready protocol | `tb_stream` output stalls | No payload mismatch or lost transaction |
| Backpressure stability | Stall schedule in `tb_stream` | Ordered scoreboard passes |
| Reset clears state | `tb_latency` reset observation | No stale valid output |
| Determinism | Repeat pytest/container run | Same PASS strings |
| Interface preservation | Icarus elaboration | Same module and ports |
