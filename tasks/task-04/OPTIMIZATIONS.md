# Optimization Notes

The baseline performs `(2r+1)^2` coordinate clamps and tuple accumulation for every output pixel, plus a temporary list of all samples. The reference uses row prefix sums for horizontal windows and then reuses those sums during the vertical pass. Edge pixels are explicitly multiplied for the repeated clamp contribution, and the divisor remains the full square window area.

This deliberately leaves algorithm choice open to the agent. SIMD, OpenMP, a specific compiler flag, or a particular library are not part of the contract.
