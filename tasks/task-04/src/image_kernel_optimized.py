"""Allocation-conscious RGB box blur using separable prefix sums."""


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

    area = (2 * radius + 1) ** 2
    horizontal = []
    for row in image:
        prefix = [[0, 0, 0]]
        for pixel in row:
            previous = prefix[-1]
            prefix.append([previous[0] + pixel[0], previous[1] + pixel[1], previous[2] + pixel[2]])
        row_sums = []
        for x in range(width):
            left = max(0, x - radius)
            right = min(width - 1, x + radius)
            total = [prefix[right + 1][c] - prefix[left][c] for c in range(3)]
            if x < radius:
                total = [total[c] + row[0][c] * (radius - x) for c in range(3)]
            right_extra = x + radius - (width - 1)
            if right_extra > 0:
                total = [total[c] + row[-1][c] * right_extra for c in range(3)]
            row_sums.append(total)
        horizontal.append(row_sums)

    output = []
    for y in range(height):
        top = max(0, y - radius)
        bottom = min(height - 1, y + radius)
        row_output = []
        for x in range(width):
            total = [sum(horizontal[source_y][x][c] for source_y in range(top, bottom + 1)) for c in range(3)]
            top_extra = radius - y if y < radius else 0
            bottom_extra = y + radius - (height - 1)
            if top_extra:
                total = [total[c] + horizontal[0][x][c] * top_extra for c in range(3)]
            if bottom_extra > 0:
                total = [total[c] + horizontal[-1][x][c] * bottom_extra for c in range(3)]
            row_output.append(tuple(value // area for value in total))
        output.append(row_output)
    return output
