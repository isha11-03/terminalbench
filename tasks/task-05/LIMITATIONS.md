# Known Limitations and Risks

- The ratio threshold is measured with wall-clock time and can vary on heavily loaded or very slow hosts; repeated medians and a 1.25x margin reduce, but do not eliminate, that risk.
- The fixture is generated in the test rather than stored as a large binary or CSV, so disk-level ingestion and peak RSS are not measured.
- The task measures throughput, not a formal peak-memory budget. The contract and tests still reject mutation and preserve bounded accumulator state.
- Five-rollout infrastructure was unavailable in this environment; rollout evidence remains `PENDING` rather than being inferred from local runs.