# Lab Template (copy for every new lab; Labs 01-05 are the worked examples)

A lab is not ready to start until every section exists. Labs 06-10 are authored by hand ahead of time; later labs are authored by `/start-lab` step 0, which follows the checklist at the end of this file.

## `README.md`
1. **Header:** track, mode, time estimate, live-API budget and who must approve it ("none" is a valid answer; see Lab 05).
2. **Systems context:** one paragraph on the boundary or failure this lab measures.
3. **Read first:** 3-6 sources with URLs. Mark which you verified and how (docs, installed package, probe). End with 2-4 questions the learner answers in `STATE.md` before predicting.
4. **Hypothesis & systems:** A (baseline) vs B (mechanism); controlled variables.
5. **Given vs yours:** list the files that ship working (domain code, wiring, fixtures, characterization tests) and the files that ship as stubs (the learner's core).
6. **Task spec:** ordered deliverables with file names; replay/static checks before any live call (`eval-standards` rule); the learner writes every core control-flow piece.
7. **Prompting thread:** which P-checkpoint this lab advances, if any.
8. **Definition of done:** the applicable Evidence Ladder rungs.
9. **Fixtures:** say which are synthetic and which are recorded.

## Other files
- `HYPOTHESIS.md`: independent variable, metrics, and a *blank* prediction. Never carry over a numeric claim (">80% cheaper") that you cannot source: Labs 02-04 each had to delete one.
- `STATE.md`: predictions log, variance analysis, checklist.
- `fixtures/`: replayable inputs. Ground truth should be proven by code where possible (Lab 04's `test_fixtures.py` derives the task answers from the store).
- `concepts.json`: 4-7 `{id, question, hint}` cards (registered when the lab is mastered).
- `src/`: stubs raising `NotImplementedError` whose docstrings are the contract, plus any given code.
- `tests/`: contract tests for the stubs, plus given tests that pass from the start (fixtures, characterization of the platform).
- `.local-reference/drills/<NN>.md` (git-ignored, examiner-only): 3 to 5 prepared defects (Category A/B) and one Category C proposal, with root causes.

## Do not
Pre-write the control-flow core, pre-fill predictions, or leave the Theory step as "Claude will explain".

## Authoring checklist
1. Read this file, the lab's existing spec, and `docs/PLATFORM_FACTS.md`. Treat the existing spec as a claim to check, not a source.
2. Re-verify every platform fact the lab depends on against the installed package or the current docs. Prefer a probe over a summary. Record what you learn in `docs/PLATFORM_FACTS.md` section 6.
3. Prefer designs that run offline: a scripted fake model (Lab 04), a fault-injecting transport under the real SDK (Lab 05), synthetic usage rows (Lab 03). Spend live tokens only where the measurement needs them, and say so in the header.
4. Write the given code, the stubs and the tests. Pin behavior in tests only where the contract is stated in a docstring.
5. Prove the tests are satisfiable: write a throwaway implementation in the scratchpad (outside the repo), run the whole suite against it, then confirm the real lab is red by design, apart from the given checks.
6. Run `uv run ruff check`, `uv run ruff format --check` and `uv run mypy --strict labs/<lab>`. Known traps: a `NamedTuple` field named `count` or `index` shadows the tuple method; exception classes need an `Error` suffix; avoid comparing a narrowed `Literal` property twice in one test.
7. Write the drill bank to `.local-reference/drills/`.
8. Update the README status table, the capability matrix and the "tests fail on purpose" line in `CLAUDE.md`. Show the user what was authored and wait for their go-ahead.
