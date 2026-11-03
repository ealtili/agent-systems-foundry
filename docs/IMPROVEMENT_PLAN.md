# Improvement Plan (2026-11-03)

Goal: make the repo teach, not just look finished. Principle: Claude supplies infrastructure and examiners; the learner writes every control-flow core.

## Phase 0 — Hygiene (autonomous)
- [x] `claude.md` -> `CLAUDE.md` (case-only rename breaks on Linux/macOS).
- [x] Fix stale docs (README layout, PROGRESS claims).

## Phase 1 — Cognitive-preservation repair (checkpoint)
Problem: ProgressMonitor, ShadowGit, ToolRegistry, models and Lab 01 `PlanExtractor` were pre-written, which removes the Build dimension for Labs 01/04/08/09.
- [x] Move `src/foundry/*` -> `reference/foundry_oracle/` (renamed package). Used only as a hidden oracle for `/drill`, never as a starting point. `src/foundry/` is now empty: you build it.
- [x] Move Lab 01 solution -> `reference/lab01_solution/`; lab `src/` is stubs raising `NotImplementedError`; tests are red by design.
- [x] Remove guessed numbers from `labs/01/HYPOTHESIS.md`; predictions now come only from you in `STATE.md`.
- [x] Oracle tests keep running in CI (`reference/tests`) so the oracle stays correct.

## Phase 2 — Deterministic mastery gate (checkpoint)
Problem: `[*]` was awarded by a model reading a markdown file.
- [x] `scripts/gate.py <lab>`: runs ruff, mypy, pytest for the lab; checks STATE.md prediction and observed values are filled in and not placeholders; checks `DEFENSE.md` exists with all five answers. Only on success it may set the lab row in PROGRESS.md. `/finish-lab` and `/verify-lab` now call it.
- [ ] (Later, per lab) add `labs/<id>/tests/test_sabotage.py` fixtures that must fail against mutated oracle code.

## Phase 3 — Enforcement instead of instruction (checkpoint)
- [x] `.claude/settings.json`: deny bare `pip`/`python`, allow `uv run` forms. Hooks deliberately NOT added: Lab 27 teaches them, so you build the real ones there.

## Phase 4 — Needs your approval / your decision (NOT done)
1. Per-track optional dependency groups in `pyproject.toml` (pyrit, playwright, tree-sitter only when Tracks E/F/D start). Dependency change = strict approval.
2. Telemetry + replay-cassette wrapper for the Anthropic client. Measuring tokens/latency is the Lab 01 learning objective; pre-building it removes that. Suggest you write it, I review.
3. Real project thread: pick a daily-use agent (e.g. PR reviewer) and tie every third lab to it.
4. Reorder: pull Labs 23-25 (rules, skills, subagents) ahead of Track C so Claude Code itself improves your workflow from week one.
5. Just-in-time labs: Labs 02-35 stay boilerplate until you reach them; each is authored when started, with a real failing test skeleton.

## Known limits
- The oracle is still in the repo; peeking is possible. The gate checks evidence, not honesty.
- Labs must be run one at a time (each has its own `src` package).

## Renumbering (2026-11-03)
Labs were renumbered into study order (see CURRICULUM.md). References to lab numbers above use the OLD numbering. New Lab 08 (replay/pass@k harness) added; old Lab 33 dropped.
