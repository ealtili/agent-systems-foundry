# Lab 09 Experimental Design

## Control Experiment
- System A (Control): Mutating source code directly on the active working tree with manual file backups.
- System B (Experiment): Capturing in-memory `git write-tree` shadow snapshots before mutating actions with O(1) instantaneous rollback on verification failure.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Shadow git snapshots allow zero-cost speculative editing and instant deterministic rollbacks without polluting commit history.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
