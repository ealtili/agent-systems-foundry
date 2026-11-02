# Lab 19 Experimental Design

## Control Experiment
- System A (Control): Ambient shell access and unrestricted filesystem tools.
- System B (Experiment): Capability-based least-privilege tokens, path-scoped jails, and taint classification on external data.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Capability-based scoping prevents lateral movement and arbitrary code execution even if the agent is fully hijacked.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
