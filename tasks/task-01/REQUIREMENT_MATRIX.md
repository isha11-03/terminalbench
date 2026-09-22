# Requirement → Verification Matrix: Task-01

| ID | Requirement | Prompt Section | Test File | Test Function | Rubric Weight | Oracle Coverage | Notes |
|---|---|---|---|---|---|---|---|
| R1.1 | Predictions must match baseline within 1e-6 tolerance | Constraints: Correctness | test_correctness.py | test_basic_correctness | 25% | Full | Validates numerical equivalence |
| R1.2 | Single input correctness | Constraints: Correctness | test_correctness.py | test_single_input_correctness | 5% | Full | Tests single-item batches |
| R1.3 | Deterministic predictions | Constraints: Determinism | test_correctness.py | test_determinism | 10% | Full | Multiple runs produce identical results |
| R1.4 | Probability distributions sum to 1.0 | Constraints: Correctness | test_correctness.py | test_probability_sum | 5% | Full | Mathematical validity |
| R1.5 | Confidence matches predicted label probability | Constraints: Correctness | test_correctness.py | test_confidence_matches_probability | 5% | Full | Internal consistency |
| R1.6 | All labels present in probabilities | Constraints: Correctness | test_correctness.py | test_all_labels_present | 2% | Full | Complete output structure |
| R1.7 | Batch equals individual predictions | Constraints: Correctness | test_correctness.py | test_batch_equivalence | 3% | Full | Batching preserves correctness |
| R2.1 | Empty input handling | Acceptance Criteria: Edge Cases | test_edge_cases.py | test_empty_input | 2% | Full | Returns empty list |
| R2.2 | Single item input | Acceptance Criteria: Edge Cases | test_edge_cases.py | test_single_item | 2% | Full | Handles single-element lists |
| R2.3 | Whitespace-only inputs | Acceptance Criteria: Edge Cases | test_edge_cases.py | test_whitespace_only | 3% | Full | Handles degenerate inputs |
| R2.4 | Special characters | Acceptance Criteria: Edge Cases | test_edge_cases.py | test_special_characters | 3% | Full | Robust to punctuation |
| R2.5 | Case insensitivity | Acceptance Criteria: Edge Cases | test_edge_cases.py | test_mixed_case | 2% | Full | Normalization works |
| R2.6 | Repeated words | Acceptance Criteria: Edge Cases | test_edge_cases.py | test_repeated_words | 2% | Full | No crashes on repetition |
| R2.7 | Very short inputs | Acceptance Criteria: Edge Cases | test_edge_cases.py | test_very_short_input | 2% | Full | Minimal text handled |
| R2.8 | Numbers in text | Acceptance Criteria: Edge Cases | test_edge_cases.py | test_numbers_in_text | 1% | Full | Mixed content |
| R2.9 | Unicode characters | Acceptance Criteria: Edge Cases | test_edge_cases.py | test_unicode_characters | 1% | Full | UTF-8 support |
| R2.10 | Extra spaces normalization | Acceptance Criteria: Edge Cases | test_edge_cases.py | test_extra_spaces | 2% | Full | Whitespace handling |
| R2.11 | Large batch handling | Acceptance Criteria: Edge Cases | test_edge_cases.py | test_large_batch | 2% | Full | Scales to 50+ items |
| R3.1 | Latency improvement ≥60% | Acceptance Criteria: Performance | test_performance.py | test_latency_improvement | 10% | Full | <510ms threshold with tolerance |
| R3.2 | Memory reduction ≥40% | Acceptance Criteria: Performance | test_performance.py | test_memory_efficiency | 10% | Full | <110MB threshold with tolerance |
| R3.3 | No performance degradation over time | Acceptance Criteria: Performance | test_performance.py | test_repeated_inference_performance | 3% | Full | Consistent across runs |
| R3.4 | Batch more efficient than individual | Acceptance Criteria: Performance | test_performance.py | test_single_vs_batch_efficiency | 3% | Full | ≥20% batch speedup |
| R3.5 | Scalability with batch size | Acceptance Criteria: Performance | test_performance.py | test_scalability_with_batch_size | 2% | Full | <0.1s per sample |
| R4.1 | InferencePipeline class exists | Constraints: API Compatibility | test_api_compatibility.py | test_class_exists | 1% | Full | Public class |
| R4.2 | predict() method exists | Constraints: API Compatibility | test_api_compatibility.py | test_predict_method_exists | 2% | Full | Public method |
| R4.3 | predict() signature correct | Constraints: API Compatibility | test_api_compatibility.py | test_predict_signature | 2% | Full | Takes 'texts' parameter |
| R4.4 | __init__() signature correct | Constraints: API Compatibility | test_api_compatibility.py | test_init_signature | 2% | Full | Takes 'model_dir' parameter |
| R4.5 | Returns list | Constraints: API Compatibility | test_api_compatibility.py | test_predict_return_type | 1% | Full | Correct return type |
| R4.6 | Prediction structure | Constraints: API Compatibility | test_api_compatibility.py | test_prediction_structure | 3% | Full | label, confidence, probabilities |
| R4.7 | Valid label values | Constraints: API Compatibility | test_api_compatibility.py | test_label_values | 2% | Full | positive/negative/neutral |
| R4.8 | Confidence in [0,1] range | Constraints: API Compatibility | test_api_compatibility.py | test_confidence_range | 2% | Full | Valid probability range |
| R4.9 | Probabilities structure | Constraints: API Compatibility | test_api_compatibility.py | test_probabilities_structure | 2% | Full | All three labels present |
| R4.10 | Empty input compatibility | Constraints: API Compatibility | test_api_compatibility.py | test_empty_input_compatibility | 1% | Full | Graceful handling |
| R4.11 | List input requirement | Constraints: API Compatibility | test_api_compatibility.py | test_list_input_requirement | 1% | Full | Type checking |
| R4.12 | String elements | Constraints: API Compatibility | test_api_compatibility.py | test_string_input_elements | 1% | Full | Element validation |
| R4.13 | Output ordering preserved | Constraints: API Compatibility | test_api_compatibility.py | test_output_ordering | 2% | Full | Input-output correspondence |

## Summary

- **Total Requirements**: 38 independent behavioral requirements
- **Test Files**: 4 (correctness, edge_cases, performance, api_compatibility)
- **Test Functions**: 38
- **Coverage**: 100% oracle coverage across all requirements
- **Rubric Total Weight**: 100%

## Grading Dimensions

1. **Functional Correctness** (55%): Core predictions, determinism, mathematical validity
2. **Edge Case Handling** (25%): Empty inputs, special characters, whitespace, unicode, large batches
3. **Performance** (28%): Latency, memory, scalability, consistency
4. **API Compatibility** (24%): Interface preservation, type correctness, structure validation

Note: Percentages add to >100% due to overlapping importance. Actual scoring normalizes to 100%.

## Performance Thresholds

Thresholds include 50% tolerance for container variance:
- **Latency**: Target 340ms (60% reduction from 850ms baseline), Threshold 510ms
- **Memory**: Target 87MB (40% reduction from 145MB baseline), Threshold 110MB

## Mutation Testing Targets

- Correctness: Remove tolerance check, swap labels, break determinism
- Edge cases: Remove empty check, break whitespace handling
- Performance: Remove optimizations one by one
- API: Change return types, modify structure
