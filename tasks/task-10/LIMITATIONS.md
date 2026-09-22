# Known Limitations

- Icarus Verilog is used for portability; no waveform artifact is required by the task.
- The construction oracle is a file-based independent implementation and is not part of the agent-facing repair contract.
- Rollout records are templates until actual benchmark rollouts occur.
- The global repository structure script currently fails on pre-existing task-02 and task-03 instruction word counts; task-10 itself meets the limit.
