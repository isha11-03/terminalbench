# QA Report

TASK-10 is a deterministic RTL repair task with a two-stage streaming datapath, signed arithmetic, active-low synchronous reset, and valid/ready backpressure. The baseline has interacting defects rather than a syntax-only failure. Tests use real simulation, boundary values, sustained traffic, stalls, and an exact latency assertion.

The image was built from scratch and the independent reference stream oracle passed in Docker. Baseline failures were observed before applying the oracle. No rollout evidence or score is invented here; the harness owns solver rollout measurement.
