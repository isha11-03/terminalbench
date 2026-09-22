# TASK-04 Summary

This benchmark asks an agent to optimize a CPU-bound RGB box blur. The baseline repeats clamped neighborhood traversal and allocates a sample list per output pixel. The reference optimization performs separable prefix-sum passes, reducing work from roughly `O(H W r^2)` to `O(H W r)` while preserving exact integer clamp semantics and the existing API.

The workload is intentionally small enough for local iteration and large enough for a timing signal. Correctness is judged independently from performance so an accidentally fast but semantically wrong implementation fails.
