# Lab 23 Experimental Design

## Control Experiment
- System A (Control): Natural language prompt instructions telling the agent to ignore malicious instructions.
- System B (Experiment): Multi-tier defense with structural XML boundary separation, canary token monitoring, and untrusted payload escaping.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Deterministic boundary defenses prevent >95% of indirect prompt injection attacks that easily bypass prompt-only defenses.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
