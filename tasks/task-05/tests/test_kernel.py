import copy
import random
import statistics
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
from src import memory_kernel, memory_kernel_baseline


def oracle(records, segment_count):
    result = [[0, [0] * 6, None, None] for _ in range(segment_count)]
    for row in records:
        segment = row[0]
        values = row[1:]
        total = sum(values)
        item = result[segment]
        item[0] += 1
        for index, value in enumerate(values):
            item[1][index] += value
        item[2] = total if item[2] is None else min(item[2], total)
        item[3] = total if item[3] is None else max(item[3], total)
    return [
        (item[0], *item[1], 0 if item[2] is None else item[2], 0 if item[3] is None else item[3])
        for item in result
    ]


def make_records(size, segment_count):
    generator = random.Random(20260922)
    return [
        (generator.randrange(segment_count), *(generator.randrange(-1000, 1001) for _ in range(6)))
        for _ in range(size)
    ]


def test_normal_and_boundary_values_match_independent_oracle():
    records = [(0, 1, -2, 3, 4, -5, 6), (2, 10, 0, 0, 0, 0, -1), (0, 2, 2, 2, 2, 2, 2)]
    assert memory_kernel.reduce_records(records, 4) == oracle(records, 4)
    assert memory_kernel_baseline.reduce_records(records, 4) == oracle(records, 4)


def test_empty_zero_segments_and_single_row_cases():
    assert memory_kernel.reduce_records([], 0) == []
    assert memory_kernel.reduce_records([], 3) == [(0, 0, 0, 0, 0, 0, 0, 0, 0)] * 3
    row = (0, 7, 7, 7, 7, 7, 7)
    assert memory_kernel.reduce_records([row], 1) == [(1, 7, 7, 7, 7, 7, 7, 42, 42)]


def test_input_is_not_mutated_and_output_is_fresh():
    records = [[1, 1, 2, 3, 4, 5, 6], [1, -1, -2, -3, -4, -5, -6]]
    before = copy.deepcopy(records)
    result = memory_kernel.reduce_records(records, 3)
    assert records == before
    result[1] = (99,)
    assert records == before


@pytest.mark.parametrize("records, count", [([(0, 1, 2)], 1), ([(2, 1, 1, 1, 1, 1, 1)], 2)])
def test_invalid_rows_are_rejected(records, count):
    with pytest.raises(ValueError):
        memory_kernel.reduce_records(records, count)
    for bad_count in (-1, 1.5, True):
        with pytest.raises(ValueError):
            memory_kernel.reduce_records([], bad_count)


def test_non_integer_and_boolean_fields_are_rejected():
    for row in [(0, 1, 2, 3, 4, 5, 1.0), (False, 1, 2, 3, 4, 5, 6)]:
        with pytest.raises(ValueError):
            memory_kernel.reduce_records([row], 1)


def test_deterministic_repeated_call_and_large_values():
    records = [(0, 10**18, -10**18, 3, 4, 5, 6)] * 3
    first = memory_kernel.reduce_records(records, 2)
    assert first == memory_kernel.reduce_records(records, 2)
    assert first[0][1:7] == (3 * 10**18, -3 * 10**18, 9, 12, 15, 18)


def test_optimized_kernel_beats_baseline_with_repeated_timings():
    records = make_records(60000, 24)
    memory_kernel.reduce_records(records, 24)
    memory_kernel_baseline.reduce_records(records, 24)
    optimized_times = []
    baseline_times = []
    for _ in range(3):
        start = time.perf_counter()
        memory_kernel.reduce_records(records, 24)
        optimized_times.append(time.perf_counter() - start)
        start = time.perf_counter()
        memory_kernel_baseline.reduce_records(records, 24)
        baseline_times.append(time.perf_counter() - start)
    optimized = statistics.median(optimized_times)
    baseline = statistics.median(baseline_times)
    assert baseline / optimized >= 1.25, (baseline, optimized)