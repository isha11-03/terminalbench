# Rollout Evidence Template: Task-01

## Rollout Configuration

**Task**: task-01 (ML Inference Pipeline Optimization)  
**Agent**: [Agent name/version]  
**Date**: [Date]  
**Container**: task-01:latest  
**Timeout**: 4 hours  
**Max Steps**: 500

## Rollout Results

### Rollout 1

**Status**: [PASS/FAIL]  
**Duration**: [HH:MM:SS]  
**Steps**: [Total agent steps]  
**Final Score**: [X/38 tests passed]

**Test Results**:
- Correctness: [X/7]
- Edge Cases: [X/11]
- Performance: [X/5]
- API Compatibility: [X/13]

**Performance Metrics**:
- Latency: [X]ms (threshold: 510ms)
- Memory: [X]MB (threshold: 110MB)

**Failure Reason** (if failed): [Description]

**Key Agent Actions**:
1. [Step count]: [Action description]
2. [Step count]: [Action description]
...

**Notes**: [Any observations]

---

### Rollout 2

[Same structure as Rollout 1]

---

### Rollout 3

[Same structure as Rollout 1]

---

### Rollout 4

[Same structure as Rollout 1]

---

### Rollout 5

[Same structure as Rollout 1]

---

## Aggregate Analysis

### Success Metrics

**Pass Rate**: [X/5] ([X]%)

**Score Distribution**:
- Full pass (38/38): [X] rollouts
- High (30-37/38): [X] rollouts
- Medium (20-29/38): [X] rollouts
- Low (<20/38): [X] rollouts
- Zero (0/38): [X] rollouts

**Average Step Count**: [X] steps (target: 100-165)

**Average Duration**: [HH:MM]

### Step Count Analysis

| Rollout | Total Steps | Exploration | Implementation | Validation | Other |
|---------|-------------|-------------|----------------|------------|-------|
| 1       | [X]         | [X]         | [X]            | [X]        | [X]   |
| 2       | [X]         | [X]         | [X]            | [X]        | [X]   |
| 3       | [X]         | [X]         | [X]            | [X]        | [X]   |
| 4       | [X]         | [X]         | [X]            | [X]        | [X]   |
| 5       | [X]         | [X]         | [X]            | [X]        | [X]   |
| **Avg** | **[X]**     | **[X]**     | **[X]**        | **[X]**    | **[X]** |

### Performance Achievement

| Rollout | Latency (ms) | Memory (MB) | Correctness | Overall |
|---------|--------------|-------------|-------------|---------|
| 1       | [X]          | [X]         | [PASS/FAIL] | [PASS/FAIL] |
| 2       | [X]          | [X]         | [PASS/FAIL] | [PASS/FAIL] |
| 3       | [X]          | [X]         | [PASS/FAIL] | [PASS/FAIL] |
| 4       | [X]          | [X]         | [PASS/FAIL] | [PASS/FAIL] |
| 5       | [X]          | [X]         | [PASS/FAIL] | [PASS/FAIL] |

### Failure Analysis

**Common Failure Patterns**:
1. [Pattern]: [X] occurrences
   - Description: [Details]
   - Root cause: [Analysis]
   - Recommendation: [Action]

2. [Pattern]: [X] occurrences
   - Description: [Details]
   - Root cause: [Analysis]
   - Recommendation: [Action]

**Test Failure Breakdown**:
| Test Category | Failures | Most Common Failing Tests |
|---------------|----------|---------------------------|
| Correctness   | [X]      | [Test names]              |
| Edge Cases    | [X]      | [Test names]              |
| Performance   | [X]      | [Test names]              |
| API Compat    | [X]      | [Test names]              |

### Grader Discrimination Analysis

**Score Spread**: [Description]
- Full marks: [X] rollouts
- Partial credit: [X] rollouts
- Zero: [X] rollouts

**Discrimination Quality**: [GOOD/FAIR/POOR]
- Rationale: [Analysis of whether grader distinguishes good/bad solutions]

**Partial Credit Analysis**:
- Do near-solutions get partial credit? [YES/NO]
- Are there cliff effects? [YES/NO]
- Does grading reflect solution quality? [YES/NO]

### Agent Behavior Patterns

**Successful Strategies** (from passing rollouts):
1. [Strategy description]
2. [Strategy description]
3. [Strategy description]

**Failed Approaches** (from failing rollouts):
1. [Approach description and why it failed]
2. [Approach description and why it failed]
3. [Approach description and why it failed]

**Common Exploration Paths**:
- [X]/5 agents started with [approach]
- [X]/5 agents used [technique]
- [X]/5 agents attempted [strategy]

### Step Count Validation

**Target**: 100-165 meaningful steps

**Actual Average**: [X] steps

**Analysis**:
- Is average within target range? [YES/NO]
- Do successful rollouts require substantial work? [YES/NO]
- Are there trivial shortcuts? [YES/NO]
- Is step count artificially inflated? [YES/NO]

**Assessment**: [MEETS TARGET / NEEDS ADJUSTMENT]

## Root Cause Analysis

### Zero-Pass Scenarios

**Count**: [X] rollouts with 0/5 success rate on specific criteria

**RCA for Each Zero-Pass Criterion**:

#### [Criterion Name]
- **Test**: [Test name]
- **Failure frequency**: [X]/5
- **Root cause**: [Analysis]
- **Is task broken?**: [YES/NO]
- **Is test broken?**: [YES/NO]
- **Is difficulty too high?**: [YES/NO]
- **Recommended action**: [Fix/adjust/accept]

### Weak Grading Criteria

**Criteria with >80% pass rate** (too easy):

#### [Criterion Name]
- **Pass rate**: [X]/5
- **Analysis**: [Why is this passing so easily?]
- **Recommended action**: [Make stricter/accept/remove]

**Criteria with <20% pass rate** (possibly too hard):

#### [Criterion Name]
- **Pass rate**: [X]/5
- **Analysis**: [Why is this failing so often?]
- **Recommended action**: [Make easier/fix/adjust expectations]

## Task Quality Assessment

### Difficulty Validation

**Empirical Difficulty**: [APPROPRIATE / TOO EASY / TOO HARD]

**Evidence**:
- Pass rate: [X]%
- Average steps: [X]
- Time to completion: [X]
- Agent feedback: [Summary]

**Comparison to Expectations**:
- Expected pass rate: 40-80%
- Actual pass rate: [X]%
- Assessment: [Analysis]

### Quality Issues Identified

1. **[Issue Category]**
   - Description: [Details]
   - Severity: [HIGH/MEDIUM/LOW]
   - Frequency: [X]/5 rollouts affected
   - Recommended fix: [Action]

2. **[Issue Category]**
   - [Same structure]

### Recommended Adjustments

#### High Priority
1. [Adjustment]: [Rationale]
2. [Adjustment]: [Rationale]

#### Medium Priority
1. [Adjustment]: [Rationale]
2. [Adjustment]: [Rationale]

#### Low Priority / Nice to Have
1. [Adjustment]: [Rationale]
2. [Adjustment]: [Rationale]

## Final Assessment

**Task Readiness**: [APPROVED / NEEDS REVISION / REJECT]

**Overall Quality**: [EXCELLENT / GOOD / FAIR / POOR]

**Key Strengths**:
1. [Strength]
2. [Strength]
3. [Strength]

**Key Weaknesses**:
1. [Weakness]
2. [Weakness]
3. [Weakness]

**Deployment Recommendation**: [DEPLOY AS-IS / DEPLOY WITH MINOR FIXES / MAJOR REVISION NEEDED / DO NOT DEPLOY]

**Rationale**: [Summary of recommendation reasoning]

---

**Completed by**: [Analyst name]  
**Date**: [Date]  
**Review status**: [DRAFT/FINAL]
