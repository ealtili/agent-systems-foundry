# Lab 04 Experimental Design

## Control Experiment
- System A (Control): Loose string argument passing parsed via regex or manual splitting.
- System B (Experiment): Strict introspected Pydantic tool schemas with automatic type coercion, input bounds checking, and deterministic error responses.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Schema introspection and type coercion eliminate parameter mismatch failures and reduce tool re-invocation attempts by >75%.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
