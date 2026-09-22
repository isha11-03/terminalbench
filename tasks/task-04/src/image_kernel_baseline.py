"""Named copy of the intentionally slow baseline used for benchmarks."""


def blur_image(image, radius=1):
	if not isinstance(radius, int) or radius < 0:
		raise ValueError("radius must be a non-negative integer")
	if not image:
		return []
	width = len(image[0])
	if any(len(row) != width for row in image):
		raise ValueError("image rows must have equal length")
	height = len(image)
	if not width or radius == 0:
		return [list(row) for row in image]
	output = []
	for y in range(height):
		row_output = []
		for x in range(width):
			samples = []
			for source_y in range(y - radius, y + radius + 1):
				clamped_y = min(height - 1, max(0, source_y))
				for source_x in range(x - radius, x + radius + 1):
					clamped_x = min(width - 1, max(0, source_x))
					samples.append(image[clamped_y][clamped_x])
			row_output.append(tuple(sum(pixel[c] for pixel in samples) // len(samples) for c in range(3)))
		output.append(row_output)
	return output


__all__ = ["blur_image"]
