"""Reliable deterministic local batch pipeline used by the oracle."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Callable


class PipelineError(RuntimeError):
    pass


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", text=True)
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(value, handle, sort_keys=True)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise


def _read_items(input_path: str | Path) -> list[dict]:
    seen: dict[str, dict] = {}
    for line in Path(input_path).read_text().splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        key = str(item["id"])
        if key in seen and seen[key] != item:
            raise ValueError(f"conflicting duplicate id: {key}")
        seen[key] = item
    return list(seen.values())


def run_batch(
    input_path: str | Path,
    state_path: str | Path,
    output_path: str | Path,
    failure_injector: Callable[[dict, int], None] | None = None,
) -> dict:
    state_file, output_file = Path(state_path), Path(output_path)
    state = recover(state_file)
    outputs = {str(row["id"]): row for row in _read_outputs(output_file)}
    for item in _read_items(input_path):
        key = str(item["id"])
        entry = state["items"].setdefault(key, {"status": "pending", "attempts": 0})
        if entry["status"] == "completed":
            if key not in outputs:
                outputs[key] = {"id": item["id"], "result": entry["result"]}
                _atomic_json(output_file, _ordered_outputs(outputs))
            continue
        entry["status"] = "running"
        entry["attempts"] += 1
        _atomic_json(state_file, state)
        try:
            if failure_injector:
                failure_injector(item, entry["attempts"])
            result = item["value"] * item["multiplier"]
            outputs[key] = {"id": item["id"], "result": result}
            _atomic_json(output_file, _ordered_outputs(outputs))
            entry.update(status="completed", result=result)
            entry.pop("error", None)
            _atomic_json(state_file, state)
        except Exception as exc:
            entry.update(status="failed", error=str(exc))
            _atomic_json(state_file, state)
            raise PipelineError(str(exc)) from exc
    _atomic_json(output_file, _ordered_outputs(outputs))
    _atomic_json(state_file, state)
    return state


def _read_outputs(path: Path) -> list[dict]:
    if not path.exists():
        return []
    value = json.loads(path.read_text())
    if not isinstance(value, list):
        raise ValueError("output must be a list")
    return value


def _ordered_outputs(outputs: dict[str, dict]) -> list[dict]:
    return [outputs[key] for key in sorted(outputs)]


def recover(state_path: str | Path) -> dict:
    path = Path(state_path)
    if not path.exists():
        return {"items": {}}
    value = json.loads(path.read_text())
    if not isinstance(value, dict) or not isinstance(value.get("items"), dict):
        raise ValueError("invalid state")
    return value


def reset(state_path: str | Path, output_path: str | Path) -> None:
    Path(state_path).unlink(missing_ok=True)
    Path(output_path).unlink(missing_ok=True)
