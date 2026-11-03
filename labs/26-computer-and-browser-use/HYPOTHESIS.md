# Lab 26 Experimental Design

## Control Experiment
- System A (Control): Raw pixel screenshot analysis with coordinate guessing.
- System B (Experiment): Accessibility tree DOM distillation combined with visual screenshot grounding and session persistence.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** DOM distillation reduces image token cost by >80% while improving element interaction accuracy from 65% to >95%.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
