# Lab 02 Experimental Hypothesis & Control Design

## A/B Control Experiment
- **System A (Control):** free-text reasoning followed by a final `ANSWER:` line, extracted by your code.
- **System B (Experiment):** provider-enforced `Verdict` schema (`answer`, `evidence`, `confidence`), validated with Pydantic v2.
- **Optional arm B0:** schema with `answer` only, to separate the format effect from the extra-fields effect.

## Experimental Parameters
- **Independent Variables:** output contract (A vs B) and `effort` (`low` vs `high`). Hold model, questions, `max_tokens` and sampling defaults constant.
- **Dependent Metrics:**
  - Accuracy against hand-verified answers (%)
  - Run-to-run agreement over k=3 (fraction of questions where all runs agree)
  - Brier score and calibration bins of stated confidence (system B only)
  - Output tokens per call (includes thinking) and round-trip latency (ms)
  - Extraction/validation failure rate (%)
- **Predicted Hypothesis:** *Intentionally blank.* Your prediction and reasoning go in `STATE.md` via `/start-lab`, BEFORE any measurement. No pre-filled numbers.
