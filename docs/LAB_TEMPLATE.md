# Lab Template (copy for every new lab; Lab 01 is the worked example)

A lab is not ready to start until every section exists. Author it just in time, before `/start-lab`.

## `README.md`
1. **Header:** track, mode, time estimate, live-API budget and who must approve it.
2. **Systems context:** one paragraph on the boundary or failure this lab measures.
3. **Read first:** 3-6 sources with URLs. Mark which you verified. End with 2-4 questions the learner answers in `STATE.md` before predicting.
4. **Hypothesis & systems:** A (baseline) vs B (mechanism); controlled variables.
5. **Task spec:** ordered deliverables with file names; replay/static checks before any live call (`eval-standards` rule); the learner writes every core control-flow piece.
6. **Prompting thread:** which P-checkpoint this lab advances, if any.
7. **Definition of done:** the applicable Evidence Ladder rungs.

## Other files
- `HYPOTHESIS.md`: independent variable, metrics, and a *blank* prediction.
- `STATE.md`: predictions log, variance analysis, checklist.
- `fixtures/`: replayable inputs (mark synthetic vs recorded).
- `concepts.json`: 4-6 `{id, question, hint}` cards (registered when the lab is mastered).
- `.local-reference/drills/<NN>.md`: 3 prepared defects (Category A/B) + one Category C proposal, with root causes. Examiner-only.
- `tests/`: only contract tests for given interfaces; the learner adds the rest.

## Do not
Pre-write the control-flow core, pre-fill predictions, or leave the Theory step as "Claude will explain".
