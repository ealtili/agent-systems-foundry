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
8. **Spaced repetition (unannounced):** run `uv run python scripts/concepts.py due --n 3 --exclude-lab <active-lab>`. Weave those questions into the lab conversation as natural check-ins, without announcing a quiz. Grade honestly and record each with `uv run python scripts/concepts.py grade <card-id> pass|fail`.
9. **Read the Lab Brief:** if `labs/<lab>/README.md` has a "Read first" list, have the user answer its questions in `STATE.md` before writing the prediction.
