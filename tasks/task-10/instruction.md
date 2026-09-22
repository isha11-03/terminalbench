# Task

Repair `src/stream_accel.sv`, a two-stage signed streaming datapath. Preserve the module name, ports, parameter, and synchronous active-low reset interface.

For every accepted input pair, compute:

`result = (a * b) + (a * 8) - (b * 2)`

The result is a signed `2*WIDTH`-bit value. The design must sustain one transfer per cycle when downstream is ready, have exactly two clock cycles from input handshake to output availability in an unstalled run, and obey valid/ready semantics under arbitrary output backpressure. A transfer occurs only when `valid && ready`; payloads must remain stable while `valid && !ready`. Reset must clear all in-flight valid state and prevent stale outputs after reset.

Use only files and tools available in the container. Do not change the public interface or tests. Run `./run-tests.sh` while diagnosing, and leave the repaired RTL in `src/stream_accel.sv`.
