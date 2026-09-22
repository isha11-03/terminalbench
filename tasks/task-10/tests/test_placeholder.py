"""Behavioral tests for the pipelined streaming RTL task."""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def run_simulation(source: str, bench: str) -> str:
    output = ROOT / "tests" / ".sim.out"
    command = ["iverilog", "-g2012", "-o", str(output), "-s", bench,
               str(ROOT / "src" / source), str(ROOT / "tests" / f"{bench}.sv")]
    compile_result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    assert compile_result.returncode == 0, compile_result.stderr
    result = subprocess.run(["vvp", str(output)], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_stream_protocol_and_arithmetic():
    output = run_simulation("stream_accel.sv", "tb_stream")
    assert "PASS stream sent=24 received=24" in output, output


def test_two_cycle_pipeline_latency():
    output = run_simulation("stream_accel.sv", "tb_latency")
    assert "PASS latency accepted=" in output, output


def test_independent_reference_oracle():
    output = run_simulation("reference_solution.sv", "tb_stream")
    assert "PASS stream sent=24 received=24" in output, output
