"""
Test functional correctness of the inference pipeline.
Validates that predictions match baseline within numerical tolerance.
"""
import pytest
import numpy as np
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from inference_pipeline import InferencePipeline


@pytest.fixture
def pipeline():
    """Create pipeline instance."""
    model_dir = Path(__file__).parent.parent / "data" / "model"
    return InferencePipeline(model_dir=str(model_dir))


@pytest.fixture
def test_data():
    """Load test data."""
    model_dir = Path(__file__).parent.parent / "data" / "model"
    with open(model_dir / "test_data.json", 'r') as f:
        return json.load(f)


@pytest.fixture
def baseline_predictions():
    """Load baseline predictions."""
    model_dir = Path(__file__).parent.parent / "data" / "model"
    with open(model_dir / "baseline_predictions.json", 'r') as f:
        return json.load(f)


def compare_predictions(pred1, pred2, tolerance=1e-6):
    """Compare two predictions with numerical tolerance."""
    if pred1['label'] != pred2['label']:
        return False
    
    # Compare confidence
    if abs(pred1['confidence'] - pred2['confidence']) > tolerance:
        return False
    
    # Compare all probabilities
    for label in pred1['probabilities']:
        if label not in pred2['probabilities']:
            return False
        diff = abs(pred1['probabilities'][label] - pred2['probabilities'][label])
        if diff > tolerance:
            return False
    
    return True


def test_basic_correctness(pipeline, test_data, baseline_predictions):
    """Test that predictions match baseline for all test samples."""
    samples = test_data['samples']
    predictions = pipeline.predict(samples)
    
    assert len(predictions) == len(baseline_predictions), \
        f"Expected {len(baseline_predictions)} predictions, got {len(predictions)}"
    
    for i, (pred, baseline) in enumerate(zip(predictions, baseline_predictions)):
        assert compare_predictions(pred, baseline), \
            f"Prediction {i} differs from baseline:\nGot: {pred}\nExpected: {baseline}"


def test_single_input_correctness(pipeline, test_data, baseline_predictions):
    """Test correctness for single inputs."""
    samples = test_data['samples']
    
    for i, sample in enumerate(samples):
        pred = pipeline.predict([sample])[0]
        baseline = baseline_predictions[i]
        
        assert compare_predictions(pred, baseline), \
            f"Single input prediction for sample {i} differs from baseline"


def test_determinism(pipeline, test_data):
    """Test that predictions are deterministic across multiple runs."""
    samples = test_data['samples']
    
    # Run prediction multiple times
    pred1 = pipeline.predict(samples)
    pred2 = pipeline.predict(samples)
    pred3 = pipeline.predict(samples)
    
    # All runs should produce identical results
    for i in range(len(samples)):
        assert compare_predictions(pred1[i], pred2[i], tolerance=0), \
            f"Predictions not deterministic at sample {i} (run 1 vs 2)"
        assert compare_predictions(pred2[i], pred3[i], tolerance=0), \
            f"Predictions not deterministic at sample {i} (run 2 vs 3)"


def test_probability_sum(pipeline, test_data):
    """Test that probabilities sum to 1.0."""
    samples = test_data['samples']
    predictions = pipeline.predict(samples)
    
    for i, pred in enumerate(predictions):
        prob_sum = sum(pred['probabilities'].values())
        assert abs(prob_sum - 1.0) < 1e-6, \
            f"Probabilities for sample {i} sum to {prob_sum}, expected 1.0"


def test_confidence_matches_probability(pipeline, test_data):
    """Test that confidence matches the probability of the predicted label."""
    samples = test_data['samples']
    predictions = pipeline.predict(samples)
    
    for i, pred in enumerate(predictions):
        label = pred['label']
        confidence = pred['confidence']
        label_prob = pred['probabilities'][label]
        
        assert abs(confidence - label_prob) < 1e-6, \
            f"Confidence {confidence} doesn't match label probability {label_prob} for sample {i}"


def test_all_labels_present(pipeline, test_data):
    """Test that all probability distributions include all labels."""
    samples = test_data['samples']
    predictions = pipeline.predict(samples)
    
    expected_labels = {'negative', 'neutral', 'positive'}
    
    for i, pred in enumerate(predictions):
        prob_labels = set(pred['probabilities'].keys())
        assert prob_labels == expected_labels, \
            f"Sample {i} missing labels: expected {expected_labels}, got {prob_labels}"


def test_batch_equivalence(pipeline, test_data):
    """Test that batch prediction equals individual predictions."""
    samples = test_data['samples']
    
    # Batch prediction
    batch_preds = pipeline.predict(samples)
    
    # Individual predictions
    individual_preds = [pipeline.predict([sample])[0] for sample in samples]
    
    # Compare
    for i in range(len(samples)):
        assert compare_predictions(batch_preds[i], individual_preds[i]), \
            f"Batch prediction differs from individual prediction at sample {i}"
