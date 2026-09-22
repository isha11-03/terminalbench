import copy
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))
from src.image_kernel import blur_image
from src.image_kernel_baseline import blur_image as baseline_blur


def oracle(image, radius):
    if radius < 0:
        raise ValueError
    if not image:
        return []
    width = len(image[0])
    if any(len(row) != width for row in image):
        raise ValueError
    output = []
    for y in range(len(image)):
        row = []
        for x in range(width):
            total = [0, 0, 0]
            for source_y in range(y - radius, y + radius + 1):
                for source_x in range(x - radius, x + radius + 1):
                    pixel = image[min(len(image) - 1, max(0, source_y))][min(width - 1, max(0, source_x))]
                    for channel in range(3):
                        total[channel] += pixel[channel]
            area = (2 * radius + 1) ** 2
            row.append(tuple(value // area for value in total))
        output.append(row)
    return output


def make_image(width, height):
    return [[((x * 29 + y * 11) % 256, (x * 7 + y * 31 + 3) % 256, (x * 13 + y * 17 + 9) % 256) for x in range(width)] for y in range(height)]


def read_ppm(path):
    values = path.read_text().split()
    if values[0] != "P3":
        raise ValueError("fixture is not P3")
    width, height, maximum = map(int, values[1:4])
    if maximum != 255:
        raise ValueError("unexpected fixture range")
    channels = list(map(int, values[4:]))
    return [[tuple(channels[(y * width + x) * 3:(y * width + x + 1) * 3]) for x in range(width)] for y in range(height)]


class KernelTests(unittest.TestCase):
    def test_normal_and_boundary_values_match_independent_oracle(self):
        for width, height, radius in ((4, 3, 1), (7, 2, 2), (2, 7, 5), (1, 1, 9)):
            image = make_image(width, height)
            self.assertEqual(blur_image(image, radius), oracle(image, radius))

    def test_empty_zero_radius_and_input_immutability(self):
        image = make_image(3, 2)
        before = copy.deepcopy(image)
        self.assertEqual(blur_image([], 4), [])
        self.assertEqual(blur_image(image, 0), image)
        self.assertEqual(image, before)
        self.assertIsNot(blur_image(image, 0), image)

    def test_validation_and_shape(self):
        with self.assertRaises(ValueError):
            blur_image([[((1, 2, 3))]], -1)
        with self.assertRaises(ValueError):
            blur_image([[(1, 2, 3)], [(4, 5, 6), (7, 8, 9)]])
        result = blur_image(make_image(5, 2), 1)
        self.assertEqual((len(result), len(result[0])), (2, 5))
        self.assertTrue(all(isinstance(pixel, tuple) and len(pixel) == 3 for row in result for pixel in row))

    def test_deterministic_repeated_call(self):
        image = make_image(9, 6)
        self.assertEqual(blur_image(image, 3), blur_image(image, 3))

    def test_baseline_reference_agrees_on_fixture_workload(self):
        image = make_image(16, 12)
        for radius in (1, 2, 4):
            self.assertEqual(blur_image(image, radius), baseline_blur(image, radius))

    def test_optimized_kernel_beats_baseline_ratio(self):
        image = make_image(96, 72)
        radius = 3
        for _ in range(1):
            blur_image(image, radius)
            baseline_blur(image, radius)
        optimized_times = []
        baseline_times = []
        for _ in range(3):
            start = time.perf_counter()
            blur_image(image, radius)
            optimized_times.append(time.perf_counter() - start)
            start = time.perf_counter()
            baseline_blur(image, radius)
            baseline_times.append(time.perf_counter() - start)
        ratio = min(baseline_times) / max(optimized_times)
        self.assertGreaterEqual(ratio, 1.4, f"optimization ratio was {ratio:.2f}x")

    def test_deterministic_ppm_fixtures(self):
        for fixture in (ROOT / "data" / "images" / "tiny.ppm", ROOT / "data" / "images" / "edge.ppm"):
            image = read_ppm(fixture)
            self.assertEqual(blur_image(image, 2), oracle(image, 2))

if __name__ == "__main__":
    unittest.main()
