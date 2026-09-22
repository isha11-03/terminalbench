# TASK-10: Pipelined Streaming Computation

A self-contained RTL repair benchmark using SystemVerilog and Icarus Verilog. The baseline intentionally contains interacting pipeline-valid, backpressure, and arithmetic-width defects. `src/reference_solution.sv` is an independent construction oracle used only by the task maintainer.

Run the baseline suite with `./run-tests.sh`. Install the oracle and verify it with `./solution.sh`. The Docker image provisions `iverilog` and runs without network access after build.
