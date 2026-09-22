"""Reference baseline: deliberately allocation-heavy RGB box blur."""


def _validate(image, radius):
    if not isinstance(radius, int) or radius < 0:
        raise ValueError("radius must be a non-negative integer")
    if not image:
        return 0
    width = len(image[0])
    if any(len(row) != width for row in image):
        raise ValueError("image rows must have equal length")
    return width


def blur_image(image, radius=1):
    """Blur an RGB image with clamp-to-edge boundaries and floor averages."""
    width = _validate(image, radius)
    height = len(image)
    if not width or not height or radius == 0:
        return [list(row) for row in image]

    output = []
    for y in range(height):
        output_row = []
        for x in range(width):
            samples = []
            for source_y in range(y - radius, y + radius + 1):
                clamped_y = min(height - 1, max(0, source_y))
                for source_x in range(x - radius, x + radius + 1):
                    clamped_x = min(width - 1, max(0, source_x))
                    samples.append(image[clamped_y][clamped_x])
            count = len(samples)
            output_row.append(tuple(sum(pixel[channel] for pixel in samples) // count for channel in range(3)))
        output.append(output_row)
    return output
