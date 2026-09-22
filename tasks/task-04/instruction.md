# TASK-04: CPU image-processing kernel optimization

Optimize `src/image_kernel.py` without changing its public API or semantics.

`blur_image(image, radius=1)` computes a box blur over a rectangular RGB image represented as a list of rows of `(red, green, blue)` integer tuples. Each channel is averaged independently with integer floor division. The window is a square of side `2 * radius + 1`; coordinates outside the image are clamped to the nearest edge pixel. The function returns a new image and must not mutate its input.

The supplied implementation is intentionally correct but inefficient. Investigate repeated neighborhood traversal, allocation behavior, and memory access patterns. Establish a baseline, profile or benchmark it, and improve it using local techniques. Do not use network access or optional native packages.

## Contract

- Preserve the callable signature and tuple/list image shape.
- Support empty images, one-pixel images, non-square images, `radius=0`, and radii larger than either dimension.
- Reject negative radii and ragged rows with `ValueError`.
- Preserve exact integer results, deterministic ordering, and input immutability.

## Validation

Use the deterministic fixtures in `data/images/`, compare against an independent reference, test boundaries and numerical behavior, and measure repeated timings on the larger fixture. The supplied tests use a ratio-based performance check with a margin for container variability.
