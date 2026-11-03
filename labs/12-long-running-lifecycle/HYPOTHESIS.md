# Lab 12 Experimental Design

## Control Experiment
- System A (Control): Continuous context accumulation leading to context overflow and lossy `/compact` summarization.
- System B (Experiment): Initializer-vs-Worker harness pattern with fresh-context session boots reading structured progress ledgers (`STATE.md`).

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Structured progress ledgers preserve 100% of critical architectural state across session boots while resetting context tokens to zero.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
