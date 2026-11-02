# Lab 07 Experimental Design

## Control Experiment
- System A (Control): Agent modifies code files and proceeds purely based on LLM self-confidence.
- System B (Experiment): Deterministic compiler backpressure where `ruff`, `mypy`, and syntax checks run automatically and inject AST diagnostics into the observation payload.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Compiler backpressure reduces syntax regression iterations by >65% and prevents syntactically broken code from persisting across agent turns.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
