# Lab 28 Experimental Design

## Control Experiment
- System A (Control): Manually copying scripts and configs across repositories.
- System B (Experiment): Versioned `.claude-plugin/plugin.json` packaging skills, hooks, and subagents with headless `claude -p` CI execution.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Plugin packaging enables portable, version-controlled agent capabilities deployed seamlessly into automated CI/CD pipelines.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
