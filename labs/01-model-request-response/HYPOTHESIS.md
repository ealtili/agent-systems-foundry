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
- **Predicted Hypothesis:**
  Enforcing strict Pydantic JSON schemas eliminates parse errors entirely (0% error rate) at an expense of ~15% token overhead and ~10% latency increase due to schema formatting.
