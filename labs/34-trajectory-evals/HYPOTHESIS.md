# Lab 34 Experimental Design

## Control Experiment
- System A (Control): Subjective manual evaluation of single agent runs.
- System B (Experiment): Automated OpenTelemetry span collection, deterministic mock-tool replay, and statistical $pass@k$ benchmarking.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Deterministic trajectory evaluation provides statistically sound reliability metrics independent of model stochasticity.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
