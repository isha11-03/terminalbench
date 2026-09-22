# Rubric

- Functional arithmetic and ordering: 30 points. Every accepted pair produces the specified signed result in order.
- Pipeline timing and throughput: 25 points. Exact two-cycle unstalled latency and one transfer per cycle under ready.
- Valid/ready behavior: 25 points. Correct acceptance, output stability during stalls, and no loss or duplication.
- Reset and boundaries: 15 points. In-flight state is flushed; negative, zero, and 16-bit extrema are correct.
- Determinism and interface: 5 points. Reproducible simulator result and unchanged public module contract.

A passing oracle suite is required; source inspection alone is insufficient.
