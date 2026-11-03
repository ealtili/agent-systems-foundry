# Lab 24 Experimental Design

## Control Experiment
- System A (Control): Fully autonomous execution with post-hoc logging.
- System B (Experiment): Policy-based execution firewalls requiring cryptographic approval tokens for high-blast-radius actions.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Policy gates bound operational risk to zero for catastrophic actions while maintaining autonomy for safe operations.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
