from pathlib import Path
root = Path(__file__).resolve().parents[1]
for n in range(1, 11):
    d = root / "tasks" / f"task-{n:02d}"
    assert d.exists()
    for f in ["Dockerfile","task.yaml","instruction.md","solution.sh","run-tests.sh"]:
        assert (d/f).exists(), f"missing {d/f}"
    assert (d/"tests").is_dir()
    assert len((d/"instruction.md").read_text().split()) <= 600
print("Structure OK")
