---
name: start-lab
description: Initialize or switch to a specific lab in the curriculum and enforce the Prediction Step.
disable-model-invocation: true
---

# Start Lab Workflow (With Mandatory Prediction Step)

When the user runs `/start-lab <lab_number_or_slug>`:
1. Locate the target lab in `labs/`.
2. Read `labs/<lab>/README.md`, `HYPOTHESIS.md`, and `STATE.md`.
3. Update `PROGRESS.md` with the active lab pointer.
4. Present a 5-line architectural brief:
   - **Hypothesis & Metric**
   - **System A (Baseline) vs System B (Experiment)**
   - **State Boundary & Trust Assumptions**
   - **Expected Failure Modes**
5. **Enforce Prediction Step:** Ask the user:
   > *"Before running any code or writing the implementation: What do you predict will happen to the dependent metric (e.g. latency, error rate, token overhead) between System A and System B, and why?"*
6. Record the user's prediction in `labs/<lab>/STATE.md` under `## Predictions`.
7. Enter Mode A or Mode B based on topic familiarity.
