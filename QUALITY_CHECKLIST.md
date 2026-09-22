# Quality Checklist

## Construction
- [ ] One coherent deep engineering problem
- [ ] Realistic local repository/environment
- [ ] Deterministic local data
- [ ] No network dependency
- [ ] No ambiguity as difficulty
- [ ] Meaningful multi-step exploration

## Prompt
- [ ] <= 600 words
- [ ] Clear objective/constraints
- [ ] Clear final-state acceptance
- [ ] No prescribed solution path

## Grading
- [ ] Functional behavior
- [ ] Edge cases
- [ ] Independent sub-capability checks
- [ ] Behavioral assertions, not grep-only
- [ ] Robust performance checks where relevant
- [ ] Determinism checks where relevant
- [ ] Requirement matrix complete

## Oracle
- [ ] Fresh build succeeds
- [ ] Oracle passes repeatedly
- [ ] Full test suite passes
- [ ] Grader does not depend on oracle artifacts

## Rollouts
- [ ] Five rollouts recorded
- [ ] Score spread reviewed
- [ ] Full-pass count reviewed
- [ ] Step count reviewed
- [ ] Failures categorized
- [ ] Zero-pass cases investigated
