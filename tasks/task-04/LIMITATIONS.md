# Limitations

- Timing is a ratio against a local Python baseline and can vary with CPU load; it is not a portable absolute throughput claim.
- Peak memory is not asserted because Python allocator behavior differs across runtimes.
- The fixtures are small deterministic P3 images; the benchmark workload is generated from a fixed formula to avoid a large opaque binary asset.
- No network rollout was performed, so deployment evidence is intentionally not claimed.