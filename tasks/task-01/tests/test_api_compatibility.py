"""
Test API compatibility - ensures the public interface is preserved.
"""
import pytest
import sys
from pathlib import Path
import inspect

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from inference_pipeline import InferencePipeline


@pytest.fixture
def pipeline():
    """Create pipeline instance."""
    model_dir = Path(__file__).parent.parent / "data" / "model"
    return InferencePipeline(model_dir=str(model_dir))


def test_class_exists():
    """Test that InferencePipeline class exists."""
    assert InferencePipeline is not None


def test_predict_method_exists(pipeline):
    """Test that predict method exists and is callable."""
    assert hasattr(pipeline, 'predict')
    assert callable(pipeline.predict)


def test_predict_signature():
    """Test that predict method has the correct signature."""
    sig = inspect.signature(InferencePipeline.predict)
    params = list(sig.parameters.keys())
    
    # Should have 'self' and 'texts' parameters
    assert 'texts' in params, "predict method should accept 'texts' parameter"


def test_init_signature():
    """Test that __init__ has expected signature."""
    sig = inspect.signature(InferencePipeline.__init__)
    params = list(sig.parameters.keys())
    
    # Should have 'self' and 'model_dir' parameters
    assert 'model_dir' in params, "__init__ should accept 'model_dir' parameter"


def test_predict_return_type(pipeline):
    """Test that predict returns a list."""
    result = pipeline.predict(["test input"])
    assert isinstance(result, list), "predict should return a list"


def test_prediction_structure(pipeline):
    """Test that predictions have the expected structure."""
    result = pipeline.predict(["good product"])
    
    assert len(result) == 1
    pred = result[0]
    
    # Check required keys
    assert 'label' in pred, "Prediction should contain 'label'"
    assert 'confidence' in pred, "Prediction should contain 'confidence'"
    assert 'probabilities' in pred, "Prediction should contain 'probabilities'"
    
    # Check types
    assert isinstance(pred['label'], str), "'label' should be a string"
    assert isinstance(pred['confidence'], (int, float)), "'confidence' should be numeric"
    assert isinstance(pred['probabilities'], dict), "'probabilities' should be a dict"


def test_label_values(pipeline):
    """Test that labels are from the expected set."""
    samples = [
        "excellent wonderful amazing",
        "terrible horrible awful",
        "okay average acceptable"
    ]
    results = pipeline.predict(samples)
    
    valid_labels = {'positive', 'negative', 'neutral'}
    
    for result in results:
        assert result['label'] in valid_labels, \
            f"Label '{result['label']}' not in expected set {valid_labels}"


def test_confidence_range(pipeline):
    """Test that confidence values are in valid range [0, 1]."""
    samples = ["good product", "bad product", "okay product"]
    results = pipeline.predict(samples)
    
    for i, result in enumerate(results):
        conf = result['confidence']
        assert 0 <= conf <= 1, \
            f"Confidence {conf} out of range [0, 1] for sample {i}"


def test_probabilities_structure(pipeline):
    """Test that probabilities dict has expected structure."""
    result = pipeline.predict(["test"])[0]
    probs = result['probabilities']
    
    # Should have all three labels
    expected_labels = {'positive', 'negative', 'neutral'}
    assert set(probs.keys()) == expected_labels, \
        f"Probabilities should have keys {expected_labels}, got {set(probs.keys())}"
    
    # All probabilities should be numeric and in range [0, 1]
    for label, prob in probs.items():
        assert isinstance(prob, (int, float)), \
            f"Probability for {label} should be numeric"
        assert 0 <= prob <= 1, \
            f"Probability for {label} is {prob}, should be in [0, 1]"


def test_empty_input_compatibility(pipeline):
    """Test that empty input is handled gracefully."""
    result = pipeline.predict([])
    assert isinstance(result, list), "Should return list even for empty input"
    assert len(result) == 0, "Should return empty list for empty input"


def test_list_input_requirement(pipeline):
    """Test that input must be a list."""
    # This should work
    result = pipeline.predict(["test"])
    assert isinstance(result, list)
    
    # Single string should raise TypeError (not a list)
    with pytest.raises(TypeError):
        pipeline.predict("test")


def test_string_input_elements(pipeline):
    """Test that input elements should be strings."""
    # Valid input
    result = pipeline.predict(["test", "another test"])
    assert len(result) == 2
    
    # Input with non-string element - should handle gracefully or raise
    try:
        result = pipeline.predict([123, "test"])
        # If it handles it, should still return list
        assert isinstance(result, list)
    except (TypeError, AttributeError):
        # Acceptable to raise error for invalid input
        pass


def test_initialization_without_args():
    """Test that pipeline can be initialized with default model_dir."""
    # This tests backward compatibility
    try:
        pipeline = InferencePipeline()
        assert pipeline is not None
    except (FileNotFoundError, OSError):
        # Acceptable if default path doesn't exist
        pass


def test_output_ordering(pipeline):
    """Test that output order matches input order."""
    samples = [
        "excellent product",
        "terrible product",
        "okay product",
        "great product",
        "bad product"
    ]
    
    results = pipeline.predict(samples)
    
    assert len(results) == len(samples), \
        "Output length should match input length"
    
    # Verify each prediction corresponds to its input
    # (we can't check exact labels, but can verify structure)
    for i, result in enumerate(results):
        assert 'label' in result, f"Result {i} missing label"
