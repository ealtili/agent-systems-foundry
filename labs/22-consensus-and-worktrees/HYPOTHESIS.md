# Lab 22 Experimental Design

## Control Experiment
- System A (Control): Multiple parallel workers mutating the same local directory.
- System B (Experiment): Isolated `git worktree` checkouts per worker with automated merge conflict adjudication by a judge agent.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Git worktree isolation completely eliminates filesystem race conditions during concurrent multi-agent code generation.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
