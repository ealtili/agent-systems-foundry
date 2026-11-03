# Improvement Plan (started 2026-11-03, updated after Lab 05)

Goal: make the repo teach, not just look finished. Principle: Claude supplies infrastructure and examiners; the learner writes every control-flow core.

## Phase 0 — Hygiene (autonomous)
- [x] `claude.md` -> `CLAUDE.md` (case-only rename breaks on Linux/macOS).
- [x] Fix stale docs (README layout, PROGRESS claims).

## Phase 1 — Cognitive-preservation repair (checkpoint)
Problem: ProgressMonitor, ShadowGit, ToolRegistry, models and Lab 01 `PlanExtractor` were pre-written, which removes the Build dimension for Labs 01/04/08/09.
- [x] Move `src/foundry/*` -> `.local-reference/foundry_oracle/` (renamed package; it started in `reference/` and moved when the repo went public, see Phase 5). Used only as a hidden oracle for `/drill`, never as a starting point. `src/foundry/` is empty: you build it.
- [x] Move the Lab 01 solution -> `.local-reference/lab01_solution/`; lab `src/` is stubs raising `NotImplementedError`; tests are red by design.
- [x] Remove guessed numbers from `labs/01/HYPOTHESIS.md`; predictions come only from you in `STATE.md`. The same rule now applies to every authored lab (Labs 02-04 each dropped an unsupported percentage from their old specs).
- [x] Oracle tests still run locally (`uv run pytest .local-reference/tests`) so the oracle stays correct. They are not part of the public repo's `uv run pytest`.

## Phase 2 — Deterministic mastery gate (checkpoint)
Problem: `[*]` was awarded by a model reading a markdown file.
- [x] `scripts/gate.py <lab>`: runs ruff, mypy, pytest for the lab; checks STATE.md prediction and observed values are filled in and not placeholders; checks `DEFENSE.md` exists with all five answers. Only on success it may set the lab row in PROGRESS.md. `/finish-lab` and `/ladder` (formerly `/verify-lab`) call it. The `--mark` path is not yet covered by tests.
- [~] Per-lab sabotage fixtures: superseded by the examiner drill banks in `.local-reference/drills/` (Labs 01-05 written), which inject a defect into the learner's own code during `/drill`.

## Phase 3 — Enforcement instead of instruction (checkpoint)
- [x] `.claude/settings.json`: deny bare `pip`/`python`, `uv add`, `uv pip` and reading `.env`; ask before `git push`. Hooks deliberately NOT added: Lab 27 teaches them, so you build the real ones there.

## Phase 4 — Decisions that needed the user
1. [x] Per-track dependency groups in `pyproject.toml` (`track-d`, `-e`, `-f`, `-h`, `-i`, `-j`), approved and added.
2. [ ] Telemetry + replay-cassette wrapper for the Anthropic client: deliberately NOT pre-built. Measuring tokens and latency is the Lab 01 and Lab 03 objective; you write it, Claude reviews.
3. [ ] Real project thread (pick a daily-use agent, tie every third lab to it): still open.
4. [x] Reorder so Claude Code itself improves your workflow earlier: done by the 2026-11-03 renumbering (see `CURRICULUM.md`).
5. [x] Just-in-time labs, decided as a hybrid: Labs 01-05 are fully authored; Labs 06-10 are to be authored by hand ahead of time; Labs 11-35 are authored by `/start-lab` step 0 (which re-verifies platform facts first and asks you to review). See `docs/LAB_TEMPLATE.md`.

## Phase 5 — Public release and authoring (2026-11-03)
- [x] Removed the copied Anthropic docs from the repo and from all history; linked them in `REFERENCES.md` instead (optional offline copies in the git-ignored `.local-docs/`).
- [x] Removed `reference/` (oracle, solutions, drill banks, answer keys) from the repo and from all history; it lives in the git-ignored `.local-reference/`.
- [x] History rewritten with `git filter-branch`; author addresses replaced by the GitHub noreply address. Published as a new public repo (https://github.com/ealtili/agent-systems-foundry) rather than force-pushing the private one, to avoid lingering objects.
- [x] README now states that this is a single-learner course, with a status table of authored vs spec-only labs.
- [x] Authored Labs 02-05 from the template. Each was checked against a throwaway reference implementation kept outside the repo, so the contract tests are proven satisfiable before they ship red.
- [x] Recorded verified API facts in `docs/PLATFORM_FACTS.md` section 6 (sampling parameters removed, caching rules, SDK retry behavior). Labs 02-04 were built on corrected facts; the old Lab 02 spec was built on `temperature`, which no longer exists.

## Known limits
- The oracle, drill banks and answer keys exist only on the author's machine (`.local-reference/`). A learner who clones the public repo has none of them, so `/drill` improvises from the lab README and Category A/B/C patterns.
- The gate checks evidence, not honesty, and it checks that the prediction fields are filled in, not that they were written first (commit your prediction before running; git history is the evidence).
- Labs must be run one at a time: each has its own `src` package.
- Local backup branches (`backup-before-rewrite`, `backup-public-prep`) still contain the removed material. Never push them.

## Renumbering (2026-11-03)
Labs were renumbered into study order (see `CURRICULUM.md`). Any lab number written in older notes or commit messages may use the OLD numbering. New Lab 08 (replay/pass@k harness) added; old Lab 33 dropped.
