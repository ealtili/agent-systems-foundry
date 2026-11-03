# Lab 14 Experimental Design

## Control Experiment
- System A (Control): Using a single high-tier reasoning model for all sub-tasks in an agent loop.
- System B (Experiment): Dynamic model tier routing dispatching cheap utility models for exploration and deep-reasoning models for architectural synthesis.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Dynamic tier routing achieves identical task success rates with >50% token cost reduction.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
