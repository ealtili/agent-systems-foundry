# Lab 05: Deadlines, Cancellation & Defensive Dispatch — State

- **Current Status:** Not Started (authored: spec, fault-injection harness, deadline/retry/breaker/fanout contract tests)
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
- [ ] G1 Static: `uv run ruff check labs/05-deadlines-and-cancellation`
- [ ] G1 Static: `uv run mypy --strict labs/05-deadlines-and-cancellation`
- [ ] G2 Functional: `uv run pytest labs/05-deadlines-and-cancellation/tests`
- [ ] G3 Replay: `analyze` reproduces results from recorded rows
- [ ] G4 Security: cancellation leaves no stray tasks; a harness bug is not swallowed
- [ ] G6 Bound: System B wall-clock stays under its deadline plus stated slack in every scenario
- [ ] G7 Defense: Passed `/defend`
