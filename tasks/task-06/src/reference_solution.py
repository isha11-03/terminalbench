"""Numerically stable reference implementation for TASK-06."""

from __future__ import annotations

import math
from typing import Iterable


def _validated(values: Iterable[float]) -> list[float]:
    result = list(values)
    if not result:
        raise ValueError("values must not be empty")
    if not all(math.isfinite(value) for value in result):
        raise ValueError("values must be finite")
    return result


def logsumexp(values: Iterable[float]) -> float:
    values = _validated(values)
    pivot = max(values)
    return pivot + math.log(sum(math.exp(value - pivot) for value in values))


def softmax(values: Iterable[float]) -> list[float]:
    values = _validated(values)
    pivot = max(values)
    weights = [math.exp(value - pivot) for value in values]
    total = math.fsum(weights)
    return [weight / total for weight in weights]


def cross_entropy(values: Iterable[float], target: int) -> float:
    values = _validated(values)
    if not isinstance(target, int) or isinstance(target, bool):
        raise TypeError("target must be an integer")
    if not 0 <= target < len(values):
        raise IndexError("target is outside values")
    return logsumexp(values) - values[target]


def main() -> None:
    import json
    import sys

    payload = json.load(sys.stdin)
    result = {
        "probabilities": softmax(payload["logits"]),
        "cross_entropy": cross_entropy(payload["logits"], payload["target"]),
    }
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"))


if __name__ == "__main__":
    main()