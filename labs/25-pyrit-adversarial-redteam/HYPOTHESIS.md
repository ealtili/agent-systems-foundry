# Lab 25 Experimental Design

## Control Experiment
- System A (Control): Manual spot-checking of prompts with hand-crafted attack strings.
- System B (Experiment): Automated adversarial red-teaming using PyRIT with custom targets, mutation converters, and multi-turn orchestrators.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Automated PyRIT mutation chains discover novel multi-turn injection vectors that manual reviews consistently miss.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
