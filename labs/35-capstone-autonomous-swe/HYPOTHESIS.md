# Lab 35 Experimental Design

## Control Experiment
- System A (Control): Naive single-prompt code generation agent.
- System B (Experiment): Production autonomous SWE agent combining AST graphs, worktree swarms, compiler backpressure, and PyRIT security gates.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** The integrated system autonomously ingests, replicates, patches, and verifies real GitHub issues while maintaining zero-trust boundaries.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
