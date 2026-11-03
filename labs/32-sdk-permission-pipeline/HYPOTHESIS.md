# Lab 32 Experimental Design

## Control Experiment
- System A (Control): Static permission flags that either allow all tools or block headless execution.
- System B (Experiment): 6-stage permission pipeline with async `can_use_tool` callbacks and `HookMatcher` dynamic input rewriting.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** The 6-stage pipeline allows dynamic policy decisions and parameter sanitization without interrupting headless execution.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
