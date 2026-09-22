# Task: Improve Embedding Retrieval and Ranking

Repair the deterministic semantic document retrieval system in this directory. It contains a corpus with precomputed embeddings, text preprocessing, embedding generation and similarity computation, a retrieval engine with metadata filters, and a public API.

Investigate and fix the reported quality, determinism, filtering, and cache problems. Documents must be ranked by true semantic similarity; equal-score ordering must be stable; category and metadata filters must be honored without unintended result loss; and changing preprocessing configuration must invalidate stale cached results. Preserve the public API and embedding dimensionality and metric.

Handle empty queries, missing data, single-result and boundary cases. Do not introduce production randomness or unnecessary performance regressions. Do not modify tests, corpus data, or data-generation code. Use only local files and dependencies.

Run `./run-tests.sh` to see failures, inspect the pipeline and tests, implement root-cause fixes, and rerun the complete suite until every behavioral test passes. Briefly document repaired behavior if repository conventions require it.
