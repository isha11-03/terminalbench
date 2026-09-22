# Requirements Document

## Introduction

The Terminal-Bench-10-Task-Assessment system is a comprehensive benchmark designed to evaluate AI agents' capabilities across multiple engineering domains. The system consists of 10 self-contained, deterministic engineering tasks that require agents to inspect local environments, understand interacting constraints, implement solutions, debug failures, and verify repository states. Each task represents a coherent, deep engineering problem with realistic complexity arising from genuine technical challenges rather than artificial ambiguity.

## Glossary

- **Benchmark_System**: The complete Terminal-Bench-10-Task-Assessment containing all 10 tasks, infrastructure, and validation tooling
- **Task**: A single self-contained engineering problem with its own container, tests, oracle solution, and grading criteria
- **Oracle**: A deterministic reference implementation (solution.sh) that correctly solves a task
- **Container**: A Docker-based isolated environment providing all dependencies, source code, and data for a task
- **Grader**: The test suite and rubric that evaluates agent solutions across multiple behavioral dimensions
- **Rollout**: A complete execution attempt by a target agent on a task, from initial container state to final verification
- **Agent**: An AI system being evaluated by the benchmark
- **Behavioral_Test**: A test that verifies actual system behavior, outputs, invariants, or measurable properties
- **Requirement_Matrix**: A mapping document that traces each requirement to its instruction, test, rubric criterion, and oracle implementation
- **Mutation_Test**: A test validation technique where intentional bugs are introduced to verify the grader detects them
- **RCA**: Root Cause Analysis of task failures or weak grading criteria
- **Acceptance_Criterion**: An observable, testable condition that defines correct task completion
- **Domain_Distribution**: The allocation of tasks across engineering domains (3 ML/AI, 2 kernel optimization, 2 scientific computing, 2 software engineering, 1 RTL)

## Requirements

### Requirement 1: Benchmark Composition

**User Story:** As a benchmark administrator, I want the system to contain exactly 10 tasks with the specified domain distribution, so that I can evaluate agents across diverse engineering capabilities.

#### Acceptance Criteria

1. THE Benchmark_System SHALL contain exactly 10 tasks
2. THE Benchmark_System SHALL contain exactly 3 tasks with domain "ml-ai"
3. THE Benchmark_System SHALL contain exactly 2 tasks with domain "kernel-optimization"
4. THE Benchmark_System SHALL contain exactly 2 tasks with domain "scientific-computing"
5. THE Benchmark_System SHALL contain exactly 2 tasks with domain "software-engineering"
6. THE Benchmark_System SHALL contain exactly 1 task with domain "rtl"
7. WHEN the domain distribution is validated, THE Benchmark_System SHALL report any deviations from the required distribution

### Requirement 2: Task Structure

**User Story:** As a benchmark administrator, I want each task to follow a consistent file structure, so that tasks are reproducible and automatable.

#### Acceptance Criteria

1. FOR ALL tasks, THE Task SHALL contain a Dockerfile
2. FOR ALL tasks, THE Task SHALL contain a task.yaml metadata file
3. FOR ALL tasks, THE Task SHALL contain an instruction.md file with word count <= 600
4. FOR ALL tasks, THE Task SHALL contain a solution.sh oracle script
5. FOR ALL tasks, THE Task SHALL contain a run-tests.sh test execution script
6. FOR ALL tasks, THE Task SHALL contain a tests/ directory
7. FOR ALL tasks, THE Task SHALL contain deterministic local data or fixtures
8. WHERE a task requires multiple coordinated services, THE Task SHALL contain a docker-compose.yaml file
9. WHEN docker-compose.yaml is absent, THE Task SHALL NOT depend on coordinated services

### Requirement 3: Task Self-Containment

**User Story:** As a benchmark user, I want each task to be fully self-contained, so that I can run tasks reliably without external dependencies.

#### Acceptance Criteria

1. FOR ALL tasks, THE Container SHALL contain all required dependencies locally
2. FOR ALL tasks, THE Container SHALL contain all required source code locally
3. FOR ALL tasks, THE Container SHALL contain all required datasets locally
4. FOR ALL tasks, THE Container SHALL contain all required configuration files locally
5. THE Task SHALL NOT require network access during execution
6. THE Task SHALL NOT require external services during execution
7. WHEN the container is built, THE Task SHALL be executable without internet connectivity

### Requirement 4: Task Determinism

**User Story:** As a benchmark administrator, I want task execution to be deterministic, so that results are reproducible and fair.

#### Acceptance Criteria

1. FOR ALL tasks, THE Task SHALL produce identical results when executed multiple times with the same agent implementation
2. WHERE random number generation is used, THE Task SHALL use deterministic seeds
3. WHERE order-dependent operations exist, THE Task SHALL control execution order
4. THE Oracle SHALL pass all tests repeatedly from a clean container
5. WHEN the Oracle is executed 5 times, THE Grader SHALL report identical scores all 5 times

### Requirement 5: Instruction Quality

**User Story:** As an agent being evaluated, I want clear task instructions, so that I understand the objective and constraints without ambiguity.

#### Acceptance Criteria

1. THE instruction.md file SHALL contain a Context section
2. THE instruction.md file SHALL contain an Objective section
3. THE instruction.md file SHALL contain a Constraints section
4. THE instruction.md file SHALL contain an Acceptance_Criteria section
5. THE instruction.md file SHALL contain a Deliverable section describing the required final repository state
6. THE instruction.md file SHALL NOT prescribe the implementation strategy
7. THE instruction.md file SHALL NOT leak oracle solution details
8. THE instruction.md file SHALL have word count <= 600 words

### Requirement 6: Grading Architecture

**User Story:** As a benchmark administrator, I want multi-dimensional grading, so that I can evaluate different aspects of agent capabilities independently.

#### Acceptance Criteria

1. FOR ALL tasks, THE Grader SHALL test functional correctness
2. FOR ALL tasks, THE Grader SHALL test edge-case handling
3. WHERE applicable, THE Grader SHALL test numerical correctness or stability
4. WHERE applicable, THE Grader SHALL test performance or resource constraints
5. WHERE applicable, THE Grader SHALL test API or interface compatibility
6. WHERE applicable, THE Grader SHALL test determinism or reproducibility
7. THE Grader SHALL use at least 3 independent behavioral dimensions per task
8. WHEN multiple dimensions exist, THE Grader SHALL report dimension scores independently

### Requirement 7: Behavioral Testing

**User Story:** As a benchmark administrator, I want tests to verify actual behavior, so that grading reflects genuine correctness rather than superficial checks.

#### Acceptance Criteria

1. FOR ALL tests, THE Behavioral_Test SHALL verify outputs, invariants, interfaces, or measurable properties
2. THE Grader SHALL NOT rely primarily on grep-based string matching
3. THE Grader SHALL NOT rely primarily on file-existence checks
4. WHERE performance is tested, THE Grader SHALL tolerate normal container variance
5. WHERE performance is tested, THE Grader SHALL detect materially incorrect implementations
6. WHEN a test fails, THE Behavioral_Test SHALL provide diagnostic information about which behavior was incorrect

### Requirement 8: Requirement Traceability

**User Story:** As a benchmark administrator, I want complete requirement traceability, so that I can verify every requirement is properly tested and implemented.

#### Acceptance Criteria

1. FOR ALL tasks, THE Requirement_Matrix SHALL map each requirement to its instruction location
2. FOR ALL tasks, THE Requirement_Matrix SHALL map each requirement to one or more tests
3. FOR ALL tasks, THE Requirement_Matrix SHALL map each requirement to rubric criteria
4. FOR ALL tasks, THE Requirement_Matrix SHALL map each requirement to oracle implementation
5. WHEN a material requirement exists, THE Requirement_Matrix SHALL contain a verification path for it

### Requirement 9: Oracle Validation

**User Story:** As a benchmark administrator, I want validated oracle solutions, so that I know tasks are solvable and tests are correct.

#### Acceptance Criteria

1. FOR ALL tasks, THE Oracle SHALL execute successfully from a clean container
2. FOR ALL tasks, THE Oracle SHALL pass the complete test suite
3. WHEN the Oracle is executed, THE Oracle SHALL complete within reasonable time bounds
4. THE Grader SHALL NOT depend on artifacts created by the Oracle
5. WHEN the container is rebuilt from scratch, THE Oracle SHALL remain functional

### Requirement 10: Mutation Testing

**User Story:** As a benchmark administrator, I want mutation-tested graders, so that I can verify tests detect incorrect implementations.

#### Acceptance Criteria

1. FOR ALL tasks, THE Mutation_Test SHALL introduce intentional bugs into the oracle solution
2. WHEN a bug is introduced, THE Grader SHALL detect the bug and report test failure
3. WHEN mutations are tested, THE Benchmark_System SHALL record which mutations were detected
4. IF a mutation is not detected, THE RCA process SHALL identify why the grader failed

### Requirement 11: Difficulty Source

**User Story:** As a benchmark designer, I want difficulty to arise from genuine engineering challenges, so that the benchmark measures real capabilities.

#### Acceptance Criteria

1. THE Task SHALL require exploration of multiple files or components
2. THE Task SHALL require understanding of interacting constraints
3. THE Task SHALL require implementation of non-trivial logic
4. THE Task SHALL require debugging of failure modes
5. THE Task SHALL require verification of final state
6. THE Task SHALL NOT create difficulty through ambiguous instructions
7. THE Task SHALL NOT create difficulty through missing requirements
8. THE Task SHALL NOT create difficulty through external network service dependencies
9. THE Task SHALL NOT create difficulty through obscure single-command tricks
10. THE Task SHALL NOT create difficulty through artificial chains of trivial subtasks

### Requirement 12: Rollout Validation

**User Story:** As a benchmark administrator, I want rollout evidence for each task, so that I can validate difficulty and grader discrimination empirically.

#### Acceptance Criteria

1. FOR ALL tasks, THE Benchmark_System SHALL execute 5 rollouts with a target agent
2. FOR ALL rollouts, THE Benchmark_System SHALL record the final score
3. FOR ALL rollouts, THE Benchmark_System SHALL record pass/fail status
4. FOR ALL rollouts, THE Benchmark_System SHALL record agent step count
5. FOR ALL rollouts, THE Benchmark_System SHALL record execution runtime
6. FOR ALL rollouts, THE Benchmark_System SHALL record failure reasons when applicable
7. WHEN rollout results show 0/5 passes, THE RCA process SHALL investigate the cause
8. WHEN rollout results show poor score distribution, THE RCA process SHALL analyze grader discrimination

### Requirement 13: Task Readiness

**User Story:** As a benchmark administrator, I want objective readiness criteria, so that I only deploy validated tasks.

#### Acceptance Criteria

1. WHEN a task is marked ready, THE Task SHALL have successfully built from scratch
2. WHEN a task is marked ready, THE Oracle SHALL have passed all tests
3. WHEN a task is marked ready, THE Mutation_Test SHALL have validated the grader
4. WHEN a task is marked ready, THE Requirement_Matrix SHALL be complete
5. WHEN a task is marked ready, 5 rollouts SHALL have been executed and analyzed
6. WHEN a task is marked ready, THE RCA SHALL have addressed any zero-pass or weak criteria

### Requirement 14: Deliverable Artifacts

**User Story:** As a benchmark administrator, I want comprehensive deliverables for each task, so that I can review and maintain the benchmark.

#### Acceptance Criteria

1. FOR ALL tasks, THE Deliverable_Artifacts SHALL include all task files (Dockerfile, task.yaml, instruction.md, tests/, solution.sh, data/)
2. FOR ALL tasks, THE Deliverable_Artifacts SHALL include the Requirement_Matrix
3. FOR ALL tasks, THE Deliverable_Artifacts SHALL include oracle validation results
4. FOR ALL tasks, THE Deliverable_Artifacts SHALL include five-rollout evidence
5. FOR ALL tasks, THE Deliverable_Artifacts SHALL include RCA documentation
6. FOR ALL tasks, THE Deliverable_Artifacts SHALL include a final readiness assessment

### Requirement 15: Agent Interaction Depth

**User Story:** As a benchmark designer, I want tasks to require substantial agent interaction, so that the benchmark measures sustained problem-solving ability.

#### Acceptance Criteria

1. WHEN a successful rollout completes, THE Agent SHALL have executed substantial meaningful steps
2. THE Task SHALL target approximately 100+ meaningful agent steps for successful difficult tasks
3. THE Task SHALL NOT artificially pad step count through trivial operations
4. WHEN rollout evidence shows very low step counts, THE RCA SHALL analyze whether the task lacks depth

### Requirement 16: Container Reproducibility

**User Story:** As a benchmark user, I want reproducible container builds, so that I can run tasks consistently across different environments.

#### Acceptance Criteria

1. WHEN a container is built, THE Container SHALL use pinned dependency versions where possible
2. WHEN a container is built multiple times, THE Container SHALL produce functionally equivalent environments
3. THE Dockerfile SHALL specify a concrete base image version
4. WHEN dependencies are installed, THE Task SHALL document any version constraints

### Requirement 17: Test Independence

**User Story:** As a benchmark administrator, I want independent test criteria, so that partial credit and diagnostic information are meaningful.

#### Acceptance Criteria

1. FOR ALL tasks, THE Grader SHALL evaluate multiple independent criteria
2. WHEN one criterion fails, THE Grader SHALL continue evaluating remaining criteria
3. WHEN tests complete, THE Grader SHALL report results for each independent criterion
4. THE Grader SHALL NOT have cascading failures where one test failure prevents subsequent tests

### Requirement 18: Performance Test Robustness

**User Story:** As a benchmark administrator, I want robust performance tests, so that legitimate solutions aren't rejected due to container variance.

#### Acceptance Criteria

1. WHERE performance is tested, THE Grader SHALL use reasonable tolerance bounds
2. WHERE performance is tested, THE Grader SHALL account for normal container execution variance
3. WHERE performance is tested, THE Grader SHALL detect implementations that are materially slower than required
4. WHERE performance is tested, THE Grader SHALL detect implementations that are materially more resource-intensive than required
5. WHEN performance tests are flaky, THE RCA SHALL identify and fix the flakiness

### Requirement 19: Task Metadata

**User Story:** As a benchmark automation system, I want structured task metadata, so that I can execute and analyze tasks programmatically.

#### Acceptance Criteria

1. THE task.yaml file SHALL specify the task id
2. THE task.yaml file SHALL specify the task name
3. THE task.yaml file SHALL specify the domain
4. THE task.yaml file SHALL specify whether the task is deterministic
5. THE task.yaml file SHALL specify whether network access is required
6. THE task.yaml file SHALL specify the instruction file path
7. THE task.yaml file SHALL specify the solution file path
8. THE task.yaml file SHALL specify the tests file path

### Requirement 20: Documentation and Guidance

**User Story:** As a benchmark maintainer, I want clear documentation, so that I can understand the design rationale and maintenance procedures.

#### Acceptance Criteria

1. THE Benchmark_System SHALL include a README explaining the overall structure
2. THE Benchmark_System SHALL include a quality checklist
3. THE Benchmark_System SHALL include requirement matrix templates
4. THE Benchmark_System SHALL include rollout record templates
5. FOR ALL tasks, THE Task SHALL include task-specific documentation explaining the design decisions
