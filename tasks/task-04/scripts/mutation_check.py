"""Small offline mutation smoke check for the independent oracle contract."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from tests.test_kernel import make_image, oracle


def mutated_clipped_divisor(image, radius):
    result = []
    for y in range(len(image)):
        row = []
        for x in range(len(image[0])):
            values = [image[sy][sx]
                     for sy in range(y - radius, y + radius + 1)
                     for sx in range(x - radius, x + radius + 1)
                     if 0 <= sy < len(image) and 0 <= sx < len(image[0])]
            row.append(tuple(sum(pixel[c] for pixel in values) // len(values) for c in range(3)))
        result.append(row)
    return result


def main():
    image = make_image(2, 2)
    expected = oracle(image, 3)
    assert mutated_clipped_divisor(image, 3) != expected, "boundary mutation was not detected"
    print("boundary/divisor mutation detected: PASS")


if __name__ == "__main__":
    main()