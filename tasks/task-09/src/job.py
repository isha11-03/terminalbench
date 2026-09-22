"""Baseline local batch pipeline. This file is intentionally unreliable."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable


class PipelineError(RuntimeError):
    pass


def _read_items(input_path: str | Path) -> list[dict]:
    return [json.loads(line) for line in Path(input_path).read_text().splitlines() if line.strip()]


def run_batch(
    input_path: str | Path,
    state_path: str | Path,
    output_path: str | Path,
    failure_injector: Callable[[dict, int], None] | None = None,
) -> dict:
    state_file = Path(state_path)
    output_file = Path(output_path)
    state = json.loads(state_file.read_text()) if state_file.exists() else {"items": {}}
    outputs = json.loads(output_file.read_text()) if output_file.exists() else []
    items = _read_items(input_path)
    for item in items:
        key = str(item["id"])
        entry = state["items"].setdefault(key, {"status": "pending", "attempts": 0})
        if entry["status"] == "completed":
            continue
        entry["status"] = "running"
        entry["attempts"] += 1
        try:
            if failure_injector:
                failure_injector(item, entry["attempts"])
            result = item["value"] * item["multiplier"]
            outputs.append({"id": item["id"], "result": result})
            entry.update(status="completed", result=result)
        except Exception as exc:
            entry.update(status="failed", error=str(exc))
            state_file.write_text(json.dumps(state, sort_keys=True))
            raise PipelineError(str(exc)) from exc
    output_file.write_text(json.dumps(outputs, sort_keys=True))
    state_file.write_text(json.dumps(state, sort_keys=True))
    return state


def recover(state_path: str | Path) -> dict:
    state_file = Path(state_path)
    return json.loads(state_file.read_text()) if state_file.exists() else {"items": {}}


def reset(state_path: str | Path, output_path: str | Path) -> None:
    Path(state_path).unlink(missing_ok=True)
    Path(output_path).unlink(missing_ok=True)
