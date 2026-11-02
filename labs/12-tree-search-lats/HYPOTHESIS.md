# Lab 12 Experimental Design

## Control Experiment
- System A (Control): Linear ReAct loop that commits irreversibly to the first explored path.
- System B (Experiment): Language Agent Tree Search (LATS) with heuristic state evaluation, branch scoring, and backtracking on dead ends.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Tree search with state backtracking solves complex algorithmic debugging tasks where greedy linear execution fails in >40% of cases.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
