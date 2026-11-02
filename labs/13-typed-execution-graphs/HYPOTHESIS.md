# Lab 13 Experimental Design

## Control Experiment
- System A (Control): Imperative while-loops with mutable dictionaries passed between functions.
- System B (Experiment): Typed execution graphs (`pydantic-graph` pattern) with immutable state models, explicit reducers, and conditional edge routers.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Typed execution graphs eliminate runtime state mutation bugs and allow static verification of unreachable states.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
