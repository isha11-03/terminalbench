# Requirement → Verification Matrix: TASK-03

## Task Overview
Embedding-based document retrieval and ranking system with intentional deficiencies in normalization, filtering, tie-handling, and caching.

## Requirements Mapping

| ID | Requirement | Instruction | Test Coverage | Oracle Fix | Validation |
|---|---|---|---|---|---|
| **R1: Core Retrieval Correctness** |||||
| R1.1 | Documents ranked by semantic similarity | "Inconsistent retrieval quality" issue | `test_retrieval_correctness.py`: 8 tests | Fixed normalization bug (normalize=True) | Verified: relevant docs in results |
| R1.2 | Similarity scores in valid range [-1, 1] | Implicit in correct retrieval | `test_scores_are_reasonable` | Fixed by normalization | Verified: scores in range |
| R1.3 | Scores decrease with rank | "Poor results" issue | `test_scores_decrease_with_rank` | Fixed by sorting logic | Verified: monotonic scores |
| **R2: Deterministic Behavior** |||||
| R2.1 | Same query returns same results | "Non-deterministic behavior" issue | `test_determinism.py`: 6 tests | Added secondary sort by doc_id | Verified: 100% deterministic |
| R2.2 | Tie-breaking is deterministic | "Different orderings" issue | `test_deterministic_ordering_with_ties` | Sort key: `(-score, doc_id)` | Verified: stable ordering |
| R2.3 | Results consistent across instances | Implicit | `test_deterministic_across_api_instances` | Fixed normalization + tie-breaking | Verified: cross-instance consistency |
| **R3: Filtering Correctness** |||||
| R3.1 | Category filter returns only matching docs | "Filtering problems" issue | `test_filtering.py`: 11 tests | Apply filters BEFORE top-k | Verified: 100% filter compliance |
| R3.2 | Filter then select top-k (not reverse) | "Fewer results than expected" | `test_filtered_results_should_match_top_k` | Reordered: filter → sort → top-k | Verified: returns requested k |
| R3.3 | Filtered results still ranked by relevance | Implicit in correct behavior | `test_filter_should_not_reduce_relevance` | Maintained sorting in filtered set | Verified: relevance preserved |
| R3.4 | Year filter works correctly | Implicit | `test_year_filter`, `test_combined_filters` | Same filtering fix | Verified: year filtering works |
| R3.5 | Min score threshold applied correctly | Implicit | `test_min_score_filter` | Applied after filtering | Verified: threshold enforced |
| **R4: Edge Cases** |||||
| R4.1 | Empty query handled gracefully | "Edge cases" requirement | `test_empty_query`, `test_whitespace_only_query` | Returns empty results | Verified: no crash |
| R4.2 | top_k=1 works correctly | Boundary condition | `test_top_k_one` | Standard path works | Verified: single result |
| R4.3 | top_k > corpus size handled | Boundary condition | `test_top_k_larger_than_corpus` | Returns all available | Verified: no overflow |
| R4.4 | Special characters processed | Robustness | `test_special_characters_in_query` | Preprocessing handles | Verified: no errors |
| R4.5 | Case insensitivity | Standard behavior | `test_case_insensitive_query` | Lowercase in preprocessing | Verified: case-insensitive |
| R4.6 | Nonexistent document returns None | API contract | `test_get_nonexistent_document` | Standard dict lookup | Verified: returns None |
| **R5: Caching Behavior** |||||
| R5.1 | Cache improves performance (behavioral) | "Cache inconsistencies" issue | `test_caching.py`: 6 tests | Cache stores results | Verified: cache works |
| R5.2 | Cache respects different parameters | Implicit correctness | `test_cache_respects_parameters` | Cache key includes all params | Verified: separate cache entries |
| R5.3 | Cache invalidated on config change | "Stale results after config change" | `test_cache_cleared_recomputes_correctly` | Added config hash tracking | Verified: cache cleared on change |
| R5.4 | System works without caching | Robustness | `test_no_cache_config` | Cache is optional | Verified: works when disabled |
| **R6: API Compatibility** |||||
| R6.1 | Search returns list of dicts | Interface contract | `test_api_compatibility.py`: 12 tests | Maintained interface | Verified: correct structure |
| R6.2 | Result structure has required fields | Interface contract | `test_search_result_structure` | Standard result object | Verified: all fields present |
| R6.3 | Ranks start at 1 and are consecutive | Standard convention | `test_rank_starts_at_one`, `test_ranks_are_consecutive` | Enumerate from 1 | Verified: ranks correct |
| R6.4 | Default parameters work | Usability | `test_default_parameters` | Defaults in function signature | Verified: optional params |
| R6.5 | get_stats returns dict | Interface contract | `test_get_stats_returns_dict` | Returns dict | Verified: dict returned |

## Bug → Fix → Test Mapping

| Bug | Root Cause | Fix | Test Detection | Oracle Verification |
|---|---|---|---|---|
| **BUG-1: Query embedding normalization** | `normalize=False` in query generation while corpus uses `normalize=True` | Changed to `normalize=True` | `test_retrieval_correctness.py` tests fail with incorrect scores | All retrieval correctness tests pass |
| **BUG-2: Same as BUG-1** | Explicit bug comment in code | Same fix as BUG-1 | Same as BUG-1 | Same as BUG-1 |
| **BUG-3: Filter after top-k** | `top_k` selection before applying category/year filters | Moved filtering logic before top-k selection | `test_filtered_results_should_match_top_k` fails (returns 3 instead of 5) | Returns correct number after filtering |
| **BUG-4: Non-deterministic ties** | No secondary sort key when scores are equal | Added secondary sort by `doc_id` | `test_deterministic_ordering_with_ties` may fail (flaky) | 100% deterministic across runs |
| **BUG-5: Cache not invalidated** | Cache key doesn't include config state | Added config hash tracking and invalidation | Tests with config changes may use stale cache | Cache cleared when config changes |

## Test Coverage Summary

| Test File | Tests | Purpose | Critical Tests |
|---|---|---|---|
| `test_retrieval_correctness.py` | 8 | Verify relevant documents ranked highly | BUG-1 detection |
| `test_determinism.py` | 6 | Ensure reproducible results | BUG-4 detection |
| `test_filtering.py` | 11 | Validate filter logic | BUG-3 detection |
| `test_edge_cases.py` | 19 | Boundary conditions and robustness | General correctness |
| `test_caching.py` | 6 | Cache behavior and consistency | BUG-5 detection |
| `test_api_compatibility.py` | 12 | Interface contracts | Regression prevention |
| **Total** | **57** | **Complete behavioral coverage** | **All bugs detectable** |

## Instruction → Test → Fix Traceability

### Issue 1: "Inconsistent Retrieval Quality"
- **Instruction**: "Some queries return unexpectedly poor results"
- **Root Cause**: Query embeddings not normalized (BUG-1, BUG-2)
- **Test Detection**: `test_neural_networks_query_returns_relevant_docs`, etc.
- **Oracle Fix**: Line 121 in solution.sh: `normalize=True`
- **Validation**: Relevant documents now appear in results

### Issue 2: "Non-Deterministic Behavior"
- **Instruction**: "Same query occasionally produces different orderings"
- **Root Cause**: No secondary sort key for ties (BUG-4)
- **Test Detection**: `test_same_query_returns_same_results`, `test_deterministic_ordering_with_ties`
- **Oracle Fix**: Lines 96-97 in solution.sh: Sort by `(-score, doc_id)`
- **Validation**: 100% deterministic across runs

### Issue 3: "Filtering Problems"
- **Instruction**: "Returns fewer results than expected when using filters"
- **Root Cause**: top-k applied before filtering (BUG-3)
- **Test Detection**: `test_filtered_results_should_match_top_k` (expects 5, gets 3)
- **Oracle Fix**: Lines 85-94 in solution.sh: Filter first, then top-k
- **Validation**: Returns requested number of filtered results

### Issue 4: "Cache Inconsistencies"
- **Instruction**: "Stale results after changing preprocessing settings"
- **Root Cause**: Cache not invalidated on config change (BUG-5)
- **Test Detection**: Implicit in `test_cache_cleared_recomputes_correctly`
- **Oracle Fix**: Lines 47-52 in solution.sh: Config hash tracking
- **Validation**: Cache cleared when config changes

## Oracle Solution Verification

✅ **All 57 tests pass** with oracle solution
✅ **All 5 bugs fixed** with targeted changes
✅ **API compatibility maintained** (no interface changes)
✅ **Deterministic behavior** verified across multiple runs
✅ **Filter logic corrected** (returns expected counts)
✅ **Cache behavior** correct with invalidation

## Grading Criteria

| Criterion | Weight | Verification Method |
|---|---|---|
| Retrieval correctness | 25% | 8 tests in `test_retrieval_correctness.py` |
| Deterministic behavior | 20% | 6 tests in `test_determinism.py` |
| Filter correctness | 20% | 11 tests in `test_filtering.py` |
| Edge case handling | 15% | 19 tests in `test_edge_cases.py` |
| Caching consistency | 10% | 6 tests in `test_caching.py` |
| API compatibility | 10% | 12 tests in `test_api_compatibility.py` |

**Passing Threshold**: 90% of tests (51/57)
**Oracle Score**: 100% (57/57)
