# Agent Systems Foundry

> **A hands-on, test-driven systems engineering laboratory for mastering Claude, the Claude Agent SDK, Model Context Protocol (MCP), and resilient multi-agent architectures.**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/package%20manager-uv-purple.svg)](https://github.com/astral-sh/uv)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy%20--strict-blue.svg)](https://mypy-lang.org/)

---

## Architectural Thesis

> **"The model is a stochastic kernel. The deterministic harness owns state, control flow, tool contracts, deadlines, verification, cost, and recovery."**

Agent Systems Foundry is not a set of passive tutorials. It is an active flight simulator designed to train you as an **AI Systems Architect**. It enforces:
1. **Cognitive Preservation:** Claude serves as an instructor, examiner, and chaos monkey—never a shortcut that completes reasoning for you.
2. **The 6-Dimension Mastery Grid:** Progress is tracked across **Explain, Build, Debug, Attack, Evaluate, and Choose**.
3. **The Evidence Ladder:** From static type safety to stochastic $pass@k$ and oral defense (`/defend`).
4. **Hermetic Execution:** Defense-in-depth isolation across filesystems, credentials, and settings provenance.

---

## Status and design

This is a **single-learner course**, built to be worked through by one person with Claude Code, not a library. It is a work in progress:

| State | Labs | What exists |
|---|---|---|
| Authored | 01-05 | Reading list, task spec, fixtures, contract tests (red until you implement), concept cards |
| Spec only | 06-35 | Hypothesis and A/B design; authored just in time |
| Planned | dynamic workflows, Managed Agents, hybrid workflow, second runtime, book-writing capstone | Drafts in `docs/planned_labs/`, unnumbered |

Labs 06-10 are meant to be authored by hand ahead of time (stable tests for the fundamentals). Labs 11-35 are authored when you run `/start-lab`, which re-verifies fast-moving platform facts first (`docs/PLATFORM_FACTS.md`) and asks you to review the result before you begin. The examiner-only answer keys and drill banks are deliberately not in this repo: they live in a git-ignored `.local-reference/` folder.

---

## Requirements

- Python 3.12+ and [uv](https://github.com/astral-sh/uv). Use `uv` for everything; bare `pip` and `python` are denied in `.claude/settings.json`.
- [Claude Code](https://code.claude.com) for the examiner workflow (`/start-lab`, `/drill`, `/defend`).
- An Anthropic API key (`ANTHROPIC_API_KEY`) only for labs that make live calls. Each lab says so in its header and asks for your approval before spending tokens. Lab 05 needs none.
- Optional per-track dependencies are `uv` dependency groups (`track-d`, `track-e`, `track-f`, `track-h`, `track-i`, `track-j`); `uv add` is denied, so you add dependencies yourself.

Licensed under MIT (`LICENSE`).

---

## Repository Layout

```text
├── CLAUDE.md                     # Lean root control plane
├── PROGRESS.md                   # 6-Dimension Mastery Grid
├── CURRICULUM.md                 # 35-Lab Catalog across Tracks A to I
├── ARCHITECTURE.md               # Core thesis, learning loop & Evidence Ladder
├── REFERENCES.md                 # Links to the official docs the course draws on
├── pyproject.toml                # uv project, dependency groups, tool config
├── docs/
│   ├── PLATFORM_FACTS.md         # Verified platform facts (re-verify before authoring)
│   ├── CAPABILITY_MATRIX.md      # Capability -> lab traceability, with honest gaps
│   ├── LAB_TEMPLATE.md           # How a lab is structured and authored
│   ├── IMPROVEMENT_PLAN.md       # What was changed and why
│   ├── planned_labs/             # Specs for labs not yet numbered
│   └── adr/                      # Architectural Decision Records (ADRs)
├── .claude/
│   ├── settings.json             # Permission rules (deny bare pip/python, uv add; ask before push)
│   ├── rules/                    # Path-scoped policies (auto-loaded via YAML globs)
│   ├── skills/                   # On-demand workflows (/start-lab, /drill, /defend, etc.)
│   └── agents/                   # Read-only subagents (architect, reviewer, redteam)
├── src/foundry/                  # YOUR harness package (built lab by lab; starts empty)
├── scripts/                      # gate.py (mastery gate, only writer of [*]), concepts.py (spaced repetition)
├── tests/                        # Repo-level tests (not lab tests)
├── labs/                         # 35 laboratories; Labs 01-05 fully authored
└── .local-reference/             # Examiner-only oracle and drill banks: git-ignored, not in the public repo
```

---

## Quickstart

```bash
# 1. Clone repository
git clone https://github.com/ealtili/agent-systems-foundry.git
cd agent-systems-foundry

# 2. Sync dependencies using uv
uv sync

# 3. Verify baseline test suite
uv run pytest                      # repo tooling tests: must be green
uv run pytest labs/01-model-request-response/tests -v   # RED by design until YOU implement Lab 01 (Labs 02-05 likewise)
uv run ruff check .
uv run mypy src tests scripts                    # repo code
uv run mypy --strict labs/01-model-request-response   # one lab at a time

# 4. Launch Claude Code
claude
```

Inside Claude Code:
- `/start-lab 01` — Checks the lab is authored (authoring it first if not), requires your prediction, and sets up the active lab.
- `/drill` — Injects intentional chaos, hidden harness defects, or adversarial payloads.
- `/ladder` — Runs the Evidence Ladder against the active lab (ruff, mypy, pytest, gate.py).
- `/audit` — Fresh read-only reviewer checks uncommitted changes against CLAUDE.md invariants.
- `/defend 01` — Conducts a 5-question oral architectural defense to qualify for `MASTERED` status.
- `/finish-lab` — Checks `/defend` was done, records your takeaway, runs `scripts/gate.py --mark` (the only thing allowed to mark a lab mastered) and advances the active-lab pointer.
- `/adr-new` — Starts an Architectural Decision Record under `docs/adr/`.
