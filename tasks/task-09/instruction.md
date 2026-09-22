# TASK-09: Stateful Data-Processing Reliability

Repair the local batch-processing component in `src/job.py` while preserving its public API: `run_batch`, `recover`, `reset`, and `PipelineError`.

The component reads JSON Lines records with `id`, `value`, and `multiplier`, tracks per-record progress in a JSON state file, and writes JSON output records. It must remain deterministic, standard-library-only at runtime, and usable without network services.

Implement behavior that remains correct across normal runs, repeated invocations, transient failures supplied through the `failure_injector` callback, duplicate input records, interrupted work, and process restarts. Identical duplicate IDs represent one logical record; conflicting duplicate payloads must be rejected without mutating persistence. Completed work must not be performed again, and a retry must preserve already completed progress while accounting for the failed record's attempt. Persisted state and output must remain valid JSON and consistent with the observable results. A completed state must be recoverable even if its corresponding output entry is missing. Stale in-progress work must be safe to resume.

Use only files and dependencies available in the container. Do not modify tests or `src/reference_solution.py`. Do not rely on network access, timing, random values, locks, or a prescribed internal file layout. Preserve deterministic output ordering and the existing API signatures.

Run `./run-tests.sh` from this directory before finishing. Acceptance is based on the supplied behavioral tests, including recovery, idempotency, duplicate handling, persistence validity, state transitions, malformed state handling, and API compatibility.
