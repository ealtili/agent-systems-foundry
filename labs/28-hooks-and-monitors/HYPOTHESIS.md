# Lab 28 Experimental Design

## Control Experiment
- System A (Control): Relying on model compliance for pre-commit linting and secret scanning.
- System B (Experiment): Deterministic `PreToolUse` and `PostToolUse` shell hooks in `settings.json` enforcing linting and blocking secrets.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Deterministic lifecycle hooks provide 100% guarantee that secrets and formatting violations never reach git.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
