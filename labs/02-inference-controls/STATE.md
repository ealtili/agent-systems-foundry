# Lab 02: Inference Controls & Observable Reasoning Artifacts — State

- **Current Status:** Not Started (authored: spec, fixtures, scoring contract tests)
- **Active Mode:** Mode A (Guided)
- **Mastery Dimensions:**
  - [ ] **E (Explain):** Mechanism and trade-offs understood.
  - [ ] **B (Build):** Implemented from scratch without copying reference code.
  - [ ] **D (Debug):** Repaired deliberate sabotage from `/drill`.
  - [ ] **A (Attack):** Defended against adversarial input.
  - [ ] **V (Evaluate):** A/B experiment measured and logged.
  - [ ] **C (Choose):** Passed oral defense (`/defend`).

## Predictions Log
- **User Prediction:** [Record prediction made during /start-lab here]
- **Observed Result:** [Record measured values here]
- **Variance Analysis:** [Explain difference between prediction and reality]

## Verification Checklist (Evidence Ladder)
- [ ] G1 Static: `uv run ruff check labs/02-inference-controls`
- [ ] G1 Static: `uv run mypy --strict labs/02-inference-controls`
- [ ] G2 Functional: `uv run pytest labs/02-inference-controls/tests`
- [ ] G3 Replay: `analyze.py` reproduces results from recorded rows
- [ ] G6 Budget: spend under the estimate you approved
- [ ] G7 Defense: Passed `/defend`
