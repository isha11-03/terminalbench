"""
Test performance and resource constraints.
Performance tests use tolerance to account for container variance.
"""
import pytest
import sys
import time
import json
from pathlib import Path
import psutil
import os

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from inference_pipeline import InferencePipeline


@pytest.fixture
def pipeline():
    """Create pipeline instance."""
    model_dir = Path(__file__).parent.parent / "data" / "model"
    return InferencePipeline(model_dir=str(model_dir))


@pytest.fixture
def test_samples():
    """Load test samples."""
    model_dir = Path(__file__).parent.parent / "data" / "model"
    with open(model_dir / "test_data.json", 'r') as f:
        data = json.load(f)
    return data['samples']


def measure_latency(pipeline, samples, runs=5):
    """Measure average latency over multiple runs."""
    latencies = []
    
    for _ in range(runs):
        start = time.time()
        pipeline.predict(samples)
        end = time.time()
        latencies.append((end - start) * 1000)  # Convert to ms
    
    return sum(latencies) / len(latencies)


def measure_memory(pipeline, samples):
    """Measure peak memory usage during inference."""
    import gc
    gc.collect()
    
    process = psutil.Process(os.getpid())
    
    # Baseline memory
    baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Run inference
    pipeline.predict(samples)
    
    # Peak memory
    peak_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    return peak_memory - baseline_memory


def test_latency_improvement(pipeline, test_samples):
    """Test that average latency meets performance target."""
    # Baseline reference: ~850ms
    # Target: 60% reduction = ~340ms
    # Allow 50% tolerance for container variance: 510ms threshold
    
    avg_latency = measure_latency(pipeline, test_samples, runs=5)
    
    threshold = 510  # ms (conservative threshold)
    
    assert avg_latency < threshold, \
        f"Average latency {avg_latency:.2f}ms exceeds threshold {threshold}ms"


def test_memory_efficiency(pipeline, test_samples):
    """Test that memory usage meets efficiency target."""
    # Baseline reference: ~145MB
    # Target: 40% reduction = ~87MB
    # Allow 50% tolerance: 110MB threshold
    
    memory_usage = measure_memory(pipeline, test_samples)
    
    threshold = 110  # MB (conservative threshold)
    
    assert memory_usage < threshold, \
        f"Memory usage {memory_usage:.2f}MB exceeds threshold {threshold}MB"


def test_repeated_inference_performance(pipeline, test_samples):
    """Test that repeated inference maintains performance."""
    latencies = []
    
    for _ in range(10):
        start = time.time()
        pipeline.predict(test_samples)
        end = time.time()
        latencies.append((end - start) * 1000)
    
    # Check that performance is consistent (no degradation)
    first_half_avg = sum(latencies[:5]) / 5
    second_half_avg = sum(latencies[5:]) / 5
    
    # Second half should not be more than 30% slower
    assert second_half_avg < first_half_avg * 1.3, \
        "Performance degraded over repeated runs"


def test_single_vs_batch_efficiency(pipeline):
    """Test that batch inference is more efficient than individual calls."""
    samples = ["good product"] * 10
    
    # Measure batch inference
    start = time.time()
    pipeline.predict(samples)
    batch_time = time.time() - start
    
    # Measure individual inference
    start = time.time()
    for sample in samples:
        pipeline.predict([sample])
    individual_time = time.time() - start
    
    # Batch should be significantly faster (at least 20% faster)
    assert batch_time < individual_time * 0.8, \
        f"Batch inference ({batch_time:.3f}s) not faster than individual ({individual_time:.3f}s)"


@pytest.mark.parametrize("batch_size", [1, 5, 10, 20])
def test_scalability_with_batch_size(pipeline, batch_size):
    """Test that performance scales reasonably with batch size."""
    samples = ["good product excellent"] * batch_size
    
    # Measure time per sample
    start = time.time()
    pipeline.predict(samples)
    total_time = time.time() - start
    
    time_per_sample = total_time / batch_size
    
    # Should process at least 10 samples per second
    assert time_per_sample < 0.1, \
        f"Time per sample {time_per_sample:.3f}s too slow for batch size {batch_size}"
