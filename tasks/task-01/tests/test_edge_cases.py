"""
Test edge case handling in the inference pipeline.
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from inference_pipeline import InferencePipeline


@pytest.fixture
def pipeline():
    """Create pipeline instance."""
    model_dir = Path(__file__).parent.parent / "data" / "model"
    return InferencePipeline(model_dir=str(model_dir))


def test_empty_input(pipeline):
    """Test that empty input returns empty output."""
    result = pipeline.predict([])
    assert result == [], "Empty input should return empty list"


def test_single_item(pipeline):
    """Test single item input."""
    result = pipeline.predict(["great product"])
    assert len(result) == 1
    assert 'label' in result[0]
    assert 'confidence' in result[0]
    assert 'probabilities' in result[0]


def test_whitespace_only(pipeline):
    """Test inputs with only whitespace."""
    inputs = ["   ", "\t\t", "\n\n", "  \t\n  "]
    results = pipeline.predict(inputs)
    
    assert len(results) == len(inputs)
    for result in results:
        assert 'label' in result
        assert 'confidence' in result
        assert 'probabilities' in result


def test_special_characters(pipeline):
    """Test inputs with special characters."""
    inputs = [
        "great!!! product!!!",
        "terrible... very bad...",
        "ok product (average quality)",
        "good product -- recommended",
        "bad product; waste of money",
    ]
    results = pipeline.predict(inputs)
    
    assert len(results) == len(inputs)
    for result in results:
        assert 'label' in result
        assert result['label'] in ['positive', 'negative', 'neutral']


def test_mixed_case(pipeline):
    """Test that predictions are case-insensitive."""
    inputs = [
        "EXCELLENT PRODUCT",
        "excellent product",
        "ExCeLlEnT pRoDuCt",
    ]
    results = pipeline.predict(inputs)
    
    # All should predict the same label
    labels = [r['label'] for r in results]
    assert len(set(labels)) == 1, "Case variations should produce same label"


def test_repeated_words(pipeline):
    """Test inputs with repeated words."""
    inputs = [
        "good good good good",
        "bad bad bad",
        "okay okay",
    ]
    results = pipeline.predict(inputs)
    
    assert len(results) == len(inputs)
    for result in results:
        assert 'label' in result


def test_very_short_input(pipeline):
    """Test very short inputs."""
    inputs = ["ok", "bad", "good", "meh"]
    results = pipeline.predict(inputs)
    
    assert len(results) == len(inputs)
    for result in results:
        assert 'label' in result
        assert 'confidence' in result


def test_numbers_in_text(pipeline):
    """Test inputs containing numbers."""
    inputs = [
        "product 123 is great",
        "version 2.0 is terrible",
        "rated 5 stars excellent",
    ]
    results = pipeline.predict(inputs)
    
    assert len(results) == len(inputs)


def test_unicode_characters(pipeline):
    """Test inputs with unicode characters."""
    inputs = [
        "great product ★★★★★",
        "terrible product ✗",
        "okay product ◐",
    ]
    results = pipeline.predict(inputs)
    
    assert len(results) == len(inputs)
    for result in results:
        assert 'label' in result


def test_extra_spaces(pipeline):
    """Test that extra spaces are handled correctly."""
    # These should be treated equivalently
    input1 = ["great  product"]  # double space
    input2 = ["great product"]   # single space
    
    result1 = pipeline.predict(input1)[0]
    result2 = pipeline.predict(input2)[0]
    
    # Should produce same label
    assert result1['label'] == result2['label']


def test_large_batch(pipeline):
    """Test handling of larger batch sizes."""
    # Generate 50 samples
    samples = ["good product"] * 25 + ["bad product"] * 25
    results = pipeline.predict(samples)
    
    assert len(results) == 50
    for result in results:
        assert 'label' in result
        assert 'confidence' in result
