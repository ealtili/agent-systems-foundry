# Lab 01 Experimental Hypothesis & Control Design

## A/B Control Experiment
- **System A (Control):** Unstructured text completions parsed via regex extraction.
- **System B (Experiment):** Enforced JSON schemas validated at the boundary via Pydantic v2.

## Experimental Parameters
- **Independent Variable:** Parsing boundary strategy (`unstructured_regex` vs `pydantic_enforced`).
- **Dependent Metrics:**
  - Parsing failure rate (%)
  - Output token count (overhead delta)
  - Round-trip latency (ms)
- **Predicted Hypothesis:** *Intentionally blank.* Your prediction and reasoning go in `STATE.md` via `/start-lab`, BEFORE any measurement. No pre-filled numbers.
