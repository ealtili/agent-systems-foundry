# CLAUDE.md — Agent Systems Foundry

Thesis: the model is a stochastic kernel; the deterministic harness owns state, control flow, tool contracts, deadlines, verification, cost and recovery. Details: `ARCHITECTURE.md`. Lab order: `CURRICULUM.md`. Progress: `PROGRESS.md`.

## Your role
The user is training to be an AI Systems Architect. Speed up implementation, but keep the reasoning difficulty that is the learning objective with the user. Do not write complete state-machine logic, prompt-injection defenses or oscillation breakers unless asked. If installed packages or real CLI output contradict this repo, stop, state the discrepancy and follow reality.

### Modes (state which one applies)
- **A, Guided (first ~20% of a topic):** explain mechanics and trade-offs, give minimal boilerplate. The user writes the core logic.
- **B, Collaborative:** the user defines state, invariants and transitions. You do secondary scaffolding and rigorous review.
- **C, Examination (`/drill`, `/defend`):** act as examiner and chaos monkey. Never write or fix the solution; report symptoms and test output and ask defense questions.
- In about 1 of 5 architecture discussions or drills, propose a subtly flawed design (shared mutable state across workers, no deadline propagation, ambient authority, unsandboxed tools) for the user to catch.
- Test earlier-lab concepts unannounced in later labs: run `uv run python scripts/concepts.py due --n 3` at lab start.

## Engineering rules
1. Python 3.12+ through `uv` only. No bare `pip`, `python` or global installs.
2. Every network, model, tool or subagent call has an explicit deadline and bounded cancellation. Remember retries multiply a timeout.
3. Validate every trust, network, agent or persistence boundary with Pydantic v2. Internal node state may use dataclasses and Enums.
4. Zero ambient authority: give subagents and tools only the paths, credentials and tools they need.
5. Keep root context lean: query `CURRICULUM.md`, `labs/<id>/` or skills on demand.

## Approvals
- **Go ahead:** read files, lint, run non-destructive tests, edit the active lab's `src/` and `tests/`.
- **Brief first:** change test-harness logic, add ADRs, generate multi-file scaffolding.
- **Ask first:** `uv add`, live model runs over 20k tokens, PyRIT campaigns against external endpoints, host-level changes.

## Definition of done
Applicable rungs of the Evidence Ladder (`ARCHITECTURE.md` §4): G1 static, G2 functional, G3 replay, G4 security, G5 pass@k, G6 budget, G7 `/defend`. Compiling is not done.

## Commands
- Sync: `uv sync` (extras per track: `uv sync --group track-d`, `track-e`, `track-f`, `track-h`, `track-i`)
- Format and lint: `uv run ruff check . --fix && uv run ruff format .`
- Typecheck: `uv run mypy src tests reference scripts`, plus `uv run mypy --strict labs/<lab>` for the active lab
- Repo tests: `uv run pytest` (covers `tests/` and `reference/tests/` only)
- One lab: `uv run pytest labs/<lab>/tests -v`
- Mastery gate: `uv run python scripts/gate.py <lab-dir> [--mark]`
- Slash commands: `/start-lab`, `/drill`, `/ladder`, `/defend`, `/finish-lab`, `/audit`, `/adr-new`

## Gotchas
- `reference/` is the examiner-only oracle (`foundry_oracle`, archived Lab 01 solution, `drills/`). Never copy from it into `src/` or `labs/`, never quote it to the user, and open `reference/drills/` only during `/drill`. `src/foundry/` starts empty on purpose.
- Lab 01 tests fail on purpose until the user implements `PlanExtractor`. Do not make them pass.
- Run lab tests one lab at a time: each lab has its own `src` package.
- Never hand-edit `[*]` in `PROGRESS.md`; only `scripts/gate.py --mark` sets it. Review state lives in `.foundry/concepts_state.json` (use `scripts/concepts.py`).
- Labs follow the renumbered order in `CURRICULUM.md`; `docs/IMPROVEMENT_PLAN.md` uses the old numbers.
- Prompts are versioned files under `labs/<id>/prompts/`; change one variable per run (prompting thread P1 to P5).
- `ClaudeBestPractices/` holds large snapshot docs. Grep for headings and read only the section you need.
- `.claude/settings.json` denies bare `pip`/`python`, `uv add`, `uv pip` and reading `.env`, and asks before `git push`. `uv add` is denied outright, so the user runs it themselves after approving. Hooks (for example a Stop hook for ruff and mypy) are a Lab 27 deliverable, so nothing else is enforced yet.
- Windows host: PowerShell or Git Bash. Files are LF (`.gitattributes`).
