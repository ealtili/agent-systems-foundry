# Lab 08 Experimental Design

## Control Experiment
- System A (Control): Naive execution loop with only a maximum iteration counter.
- System B (Experiment): `ProgressMonitor` tracking exact tool repetition (`ExactStateRepeater`) and alternating multi-step cycles (`CycleDetector`).

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Trajectory-based cycle detection identifies livelocks (e.g. S1 -> S2 -> S1) in <3 steps, saving >70% of wasted budget compared to max-step caps.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
