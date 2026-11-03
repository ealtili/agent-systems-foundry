# Lab 04: In-Process Tool Execution & ACI Design — State

- **Current Status:** Not Started (authored: spec, fixtures, registry/dispatch/loop/scoring contract tests)
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
- [ ] G1 Static: `uv run ruff check labs/04-inprocess-tool-dispatch`
- [ ] G1 Static: `uv run mypy --strict labs/04-inprocess-tool-dispatch`
- [ ] G2 Functional: `uv run pytest labs/04-inprocess-tool-dispatch/tests`
- [ ] G3 Replay: `analyze` reproduces results from recorded rows
- [ ] G4 Security: a handler bug crashes the harness and never reaches the model
- [ ] G6 Budget: spend under the estimate you approved
- [ ] G7 Defense: Passed `/defend`
