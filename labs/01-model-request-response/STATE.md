# Lab 01 Active State & Mastery Record

- **Current Status:** In Progress
- **Active Mode:** Mode A (Guided)
- **Mastery Dimensions:**
  - [ ] **E (Explain):** Trade-off between schema overhead and downstream determinism.
  - [ ] **B (Build):** `PlanExtractor` and schema validation implemented.
  - [ ] **D (Debug):** Repaired trailing markdown fence and truncated JSON failures.
  - [ ] **A (Attack):** Handled prompt injection attempting to violate schema types.
  - [ ] **V (Evaluate):** A/B benchmark completed with recorded latency and token count.
  - [ ] **C (Choose):** Completed `/defend 01` defense on when to use raw text vs structured output.

## Predictions Log
- **User Prediction:** [Record prediction made during /start-lab here]
- **Observed Result:** [Record measured values here]
- **Variance Analysis:** [Explain any difference between prediction and reality]

## Verification Checklist (Evidence Ladder)
- [ ] G1 Static: `uv run ruff check labs/01-model-request-response`
- [ ] G1 Static: `uv run mypy --strict labs/01-model-request-response`
- [ ] G2 Functional: `uv run pytest labs/01-model-request-response/tests`
- [ ] G3 Behavioral: Trajectory replay test verified
- [ ] G5 Budget: In-budget verification (< 2000 tokens)
- [ ] G7 Defense: Passed `/defend 01`
