# Lab 16 Experimental Design

## Control Experiment
- System A (Control): Direct point-to-point agent message passing.
- System B (Experiment): Shared blackboard state store with optimistic concurrency control (`version_id`) and topic subscriptions.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Optimistic concurrency on a shared blackboard prevents race conditions and data overwrites between parallel agents.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
