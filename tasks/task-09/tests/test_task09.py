from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
import job


INPUT = Path(__file__).parents[1] / "data" / "input.jsonl"
CONFLICTING = Path(__file__).parents[1] / "data" / "conflicting.jsonl"


def paths(tmp_path: Path) -> tuple[Path, Path]:
    return tmp_path / "state.json", tmp_path / "output.json"


def read(path: Path):
    return json.loads(path.read_text())


def test_normal_processing_is_complete_and_ordered(tmp_path):
    state_path, output_path = paths(tmp_path)
    state = job.run_batch(INPUT, state_path, output_path)
    assert read(output_path) == [
        {"id": "a", "result": 21},
        {"id": "b", "result": 20},
        {"id": "c", "result": 18},
    ]
    assert all(item["status"] == "completed" for item in state["items"].values())
    assert all(item["attempts"] == 1 for item in state["items"].values())


def test_identical_duplicate_input_is_processed_once(tmp_path):
    state_path, output_path = paths(tmp_path)
    job.run_batch(INPUT, state_path, output_path)
    assert len(read(output_path)) == 3
    assert read(state_path)["items"]["b"]["attempts"] == 1


def test_conflicting_duplicate_is_rejected_before_mutation(tmp_path):
    state_path, output_path = paths(tmp_path)
    with pytest.raises(ValueError, match="conflicting duplicate"):
        job.run_batch(CONFLICTING, state_path, output_path)
    assert not state_path.exists()
    assert not output_path.exists()


def test_retry_preserves_progress_and_increments_only_failed_item(tmp_path):
    state_path, output_path = paths(tmp_path)
    failed = {"b": False}

    def fail_b_once(item, attempt):
        if item["id"] == "b" and not failed["b"]:
            failed["b"] = True
            raise OSError("temporary write interruption")

    with pytest.raises(job.PipelineError):
        job.run_batch(INPUT, state_path, output_path, fail_b_once)
    first = read(state_path)
    assert first["items"]["a"]["status"] == "completed"
    assert first["items"]["b"]["status"] == "failed"
    assert first["items"]["a"]["attempts"] == 1

    state = job.run_batch(INPUT, state_path, output_path, fail_b_once)
    assert state["items"]["a"]["attempts"] == 1
    assert state["items"]["b"]["attempts"] == 2
    assert len(read(output_path)) == 3


def test_rerun_is_idempotent(tmp_path):
    state_path, output_path = paths(tmp_path)
    first = job.run_batch(INPUT, state_path, output_path)
    first_output = read(output_path)
    second = job.run_batch(INPUT, state_path, output_path)
    assert second == first
    assert read(output_path) == first_output


def test_completed_state_repairs_missing_output_without_reprocessing(tmp_path):
    state_path, output_path = paths(tmp_path)
    job.run_batch(INPUT, state_path, output_path)
    output_path.write_text(json.dumps([{"id": "a", "result": 21}]))
    job.run_batch(INPUT, state_path, output_path)
    assert read(state_path)["items"]["b"]["attempts"] == 1
    assert read(output_path) == [
        {"id": "a", "result": 21},
        {"id": "b", "result": 20},
        {"id": "c", "result": 18},
    ]


def test_restart_reprocesses_stale_running_item(tmp_path):
    state_path, output_path = paths(tmp_path)
    state_path.write_text(json.dumps({"items": {"a": {"status": "running", "attempts": 1}}}))
    job.run_batch(INPUT, state_path, output_path)
    assert read(state_path)["items"]["a"]["status"] == "completed"
    assert read(state_path)["items"]["a"]["attempts"] == 2


def test_malformed_persistence_is_rejected(tmp_path):
    state_path, output_path = paths(tmp_path)
    state_path.write_text("[]")
    with pytest.raises(ValueError, match="invalid state"):
        job.run_batch(INPUT, state_path, output_path)


def test_recover_and_reset_public_api(tmp_path):
    state_path, output_path = paths(tmp_path)
    assert job.recover(state_path) == {"items": {}}
    job.run_batch(INPUT, state_path, output_path)
    assert job.recover(state_path)["items"]["c"]["result"] == 18
    job.reset(state_path, output_path)
    assert job.recover(state_path) == {"items": {}}
    assert not output_path.exists()


def test_failure_leaves_valid_json_persistence(tmp_path):
    state_path, output_path = paths(tmp_path)

    def always_fail(item, attempt):
        raise RuntimeError("nope")

    with pytest.raises(job.PipelineError):
        job.run_batch(INPUT, state_path, output_path, always_fail)
    assert isinstance(read(state_path), dict)
    assert read(state_path)["items"]["a"]["status"] == "failed"
