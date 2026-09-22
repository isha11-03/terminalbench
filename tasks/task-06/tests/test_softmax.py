import json
import math
import pathlib
import subprocess
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parents[1] / "src"))
import softmax


def reference_logsumexp(values):
    pivot = max(values)
    return pivot + math.log(sum(math.exp(value - pivot) for value in values))


def test_ordinary_probabilities_and_loss():
    probabilities = softmax.softmax([1.0, 2.0, 3.0])
    assert probabilities == pytest.approx([0.09003057317038046, 0.24472847105479764, 0.6652409557748218])
    assert sum(probabilities) == pytest.approx(1.0, abs=1e-15)
    assert softmax.cross_entropy([1.0, 2.0, 3.0], 2) == pytest.approx(-math.log(probabilities[2]))


def test_extreme_logits_are_finite_and_shift_invariant():
    for values in ([1000.0, 999.0, 998.0], [-1000.0, -1001.0, -1002.0], [-745.0, -744.0, 0.0, 709.0]):
        probabilities = softmax.softmax(values)
        shifted = softmax.softmax([value - 5000.0 for value in values])
        assert all(math.isfinite(value) and 0.0 <= value <= 1.0 for value in probabilities)
        assert sum(probabilities) == pytest.approx(1.0, abs=1e-15)
        assert probabilities == pytest.approx(shifted, rel=1e-14, abs=1e-15)
        assert softmax.logsumexp(values) == pytest.approx(reference_logsumexp(values), rel=1e-14)


def test_cross_entropy_uses_logsumexp_without_probability_underflow():
    values = [0.0, -1000.0]
    assert softmax.cross_entropy(values, 1) == pytest.approx(1000.0, rel=1e-14)


@pytest.mark.parametrize("values", [[], [math.inf], [math.nan], [-math.inf]])
def test_rejects_empty_or_nonfinite_values(values):
    with pytest.raises(ValueError):
        softmax.softmax(values)
    with pytest.raises(ValueError):
        softmax.logsumexp(values)


def test_rejects_invalid_targets():
    with pytest.raises(IndexError):
        softmax.cross_entropy([1.0, 2.0], 2)
    with pytest.raises(TypeError):
        softmax.cross_entropy([1.0, 2.0], 0.5)


def test_cli_is_deterministic_and_matches_api():
    payload = {"logits": [1000.0, 999.0, 998.0], "target": 0}
    completed = subprocess.run(
        [sys.executable, "src/softmax.py"],
        input=json.dumps(payload), text=True, capture_output=True, check=True,
    )
    result = json.loads(completed.stdout)
    assert result["probabilities"] == pytest.approx(softmax.softmax(payload["logits"]))
    assert result["cross_entropy"] == pytest.approx(softmax.cross_entropy(payload["logits"], 0))
    assert completed.stdout == subprocess.run(
        [sys.executable, "src/softmax.py"],
        input=json.dumps(payload), text=True, capture_output=True, check=True,
    ).stdout


def test_deterministic_data_cases_are_covered():
    cases = json.loads((pathlib.Path(__file__).parents[1] / "data/cases.json").read_text())
    assert [case["name"] for case in cases] == ["ordinary", "large_positive", "large_negative", "wide_range"]