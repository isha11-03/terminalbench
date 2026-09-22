"""Correct but allocation-heavy baseline for the benchmark."""


def reduce_records(records, segment_count):
    if isinstance(segment_count, bool) or not isinstance(segment_count, int) or segment_count < 0:
        raise ValueError("segment_count must be a non-negative integer")
    rows = list(records)
    if segment_count == 0 and rows:
        raise ValueError("segment_count must be positive for non-empty input")
    accumulators = {}
    for raw_row in rows:
        row = tuple(raw_row)
        if len(row) != 7:
            raise ValueError("each row must contain seven integers")
        if any(isinstance(value, bool) or not isinstance(value, int) for value in row):
            raise ValueError("each row field must be an integer")
        segment = row[0]
        if segment < 0 or segment >= segment_count:
            raise ValueError("segment id is out of range")
        values = list(row[1:])
        total = sum(values)
        if segment not in accumulators:
            accumulators[segment] = {"count": 0, "sums": [0] * 6, "min": total, "max": total}
        item = accumulators[segment]
        item["count"] += 1
        item["sums"] = [left + right for left, right in zip(item["sums"], values)]
        item["min"] = min(item["min"], total)
        item["max"] = max(item["max"], total)
    result = []
    for segment in range(segment_count):
        item = accumulators.get(segment)
        if item is None:
            result.append((0, 0, 0, 0, 0, 0, 0, 0, 0))
        else:
            result.append((item["count"], *item["sums"], item["min"], item["max"]))
    return result