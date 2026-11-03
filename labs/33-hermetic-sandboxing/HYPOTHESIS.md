# Lab 33 Experimental Design

## Control Experiment
- System A (Control): Running Agent SDK instances with ambient host filesystem access and default setting sources.
- System B (Experiment): Hermetic multi-tenant containers with `setting_sources=[]`, isolated `cwd`, and per-tenant credential injection.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Explicit setting sources isolation (`setting_sources=[]`) prevents cross-tenant configuration bleed and data leakage.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
