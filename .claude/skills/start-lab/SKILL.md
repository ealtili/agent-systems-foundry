---
name: start-lab
description: Initialize or switch to a specific lab in the curriculum and enforce the Prediction Step.
disable-model-invocation: true
---

# Start Lab Workflow (With Mandatory Prediction Step)

**Step 0: is the lab authored?** A lab is authored when it has a README "Read first" list, `fixtures/`, `concepts.json` and contract tests under `tests/` (Labs 01-02 are; see the README status table). If not, stop and run the authoring step before anything else:
1. Say so and read `docs/LAB_TEMPLATE.md` and the lab's `README.md`/`HYPOTHESIS.md`.
2. Re-verify every platform claim the lab depends on against the installed package or current docs (`docs/PLATFORM_FACTS.md` says which products move fast). Do not trust memory or the existing spec text: Lab 02's old spec assumed `temperature`, which no longer exists.
3. Author only what the template lists: reading list, controlled variables, task spec, fixtures (mark synthetic vs recorded), `concepts.json`, contract tests for given interfaces, stubs raising `NotImplementedError`. Never write the control-flow core, and never pre-fill predictions.
4. Prove the tests are satisfiable with a throwaway implementation kept OUTSIDE the repo (scratchpad), then confirm the real lab's tests are red by design.
5. Put the drill bank in `.local-reference/drills/` (git-ignored, examiner-only).
6. Show the user a summary of what was authored and the facts you verified, and wait for their go-ahead before continuing with the steps below. Authored labs are reviewed by the user once; do not re-author on every start.

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
