"""Reference optimized implementation for the segmented reduction."""


def reduce_records(records, segment_count):
    if isinstance(segment_count, bool) or not isinstance(segment_count, int) or segment_count < 0:
        raise ValueError("segment_count must be a non-negative integer")
    accumulators = [[0, 0, 0, 0, 0, 0, 0, None, None] for _ in range(segment_count)]
    seen_rows = False
    for row in records:
        if len(row) != 7:
            raise ValueError("each row must contain seven integers")
        if any(isinstance(value, bool) or not isinstance(value, int) for value in row):
            raise ValueError("each row field must be an integer")
        segment = row[0]
        if segment < 0 or segment >= segment_count:
            raise ValueError("segment id is out of range")
        seen_rows = True
        item = accumulators[segment]
        value_0, value_1, value_2, value_3, value_4, value_5 = row[1:]
        total = value_0 + value_1 + value_2 + value_3 + value_4 + value_5
        item[0] += 1
        item[1] += value_0
        item[2] += value_1
        item[3] += value_2
        item[4] += value_3
        item[5] += value_4
        item[6] += value_5
        if item[7] is None or total < item[7]:
            item[7] = total
        if item[8] is None or total > item[8]:
            item[8] = total
    if segment_count == 0:
        if seen_rows:
            raise ValueError("segment_count must be positive for non-empty input")
        return []
    return [
        (item[0], item[1], item[2], item[3], item[4], item[5], item[6],
         0 if item[7] is None else item[7], 0 if item[8] is None else item[8])
        for item in accumulators
    ]