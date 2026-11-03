# Claude Agent Foundry

> **A hands-on, test-driven systems engineering laboratory for mastering Claude, the Claude Agent SDK, Model Context Protocol (MCP), and resilient multi-agent architectures.**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/package%20manager-uv-purple.svg)](https://github.com/astral-sh/uv)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy%20--strict-blue.svg)](https://mypy-lang.org/)

---

## Architectural Thesis

> **"The model is a stochastic kernel. The deterministic harness owns state, control flow, tool contracts, deadlines, verification, cost, and recovery."**

Claude Agent Foundry is not a set of passive tutorials. It is an active flight simulator designed to train you as an **AI Systems Architect**. It enforces:
1. **Cognitive Preservation:** Claude serves as an instructor, examiner, and chaos monkey—never a shortcut that completes reasoning for you.
2. **The 6-Dimension Mastery Grid:** Progress is tracked across **Explain, Build, Debug, Attack, Evaluate, and Choose**.
3. **The Evidence Ladder:** From static type safety to stochastic $pass@k$ and oral defense (`/defend`).
4. **Hermetic Execution:** Defense-in-depth isolation across filesystems, credentials, and settings provenance.

---

## Repository Layout

```text
├── CLAUDE.md                     # Lean root control plane
├── PROGRESS.md                   # 6-Dimension Mastery Grid 
├── CURRICULUM.md                 # 35-Lab Catalog across Tracks A to I
├── ARCHITECTURE.md               # Core thesis, learning loop & Evidence Ladder
├── pyproject.toml                # uv workspace configuration
├── docs/adr/                     # Architectural Decision Records (ADRs)
├── .claude/
│   ├── rules/                    # Path-scoped policies (auto-loaded via YAML globs)
│   ├── skills/                   # On-demand workflows (/start-lab, /drill, /defend, etc.)
│   ├── agents/                   # Context-isolated subagents (architect, reviewer, redteam)
├── src/foundry/                  # YOUR harness package (built lab by lab; starts empty)
├── .local-reference/             # Examiner-only oracle, git-ignored, not in the public repo
├── scripts/gate.py               # Deterministic mastery gate (only writer of [*])
└── labs/                         # 35 Hands-on experimental laboratories
```

---

## Quickstart

```bash
# 1. Clone repository
git clone https://github.com/<your-username>/claude-agent-foundry.git
cd claude-agent-foundry

# 2. Sync dependencies using uv
uv sync

# 3. Verify baseline test suite
uv run pytest                      # oracle + tooling: must be green
uv run pytest labs/01-model-request-response/tests -v   # RED by design until YOU implement Lab 01
uv run ruff check .
uv run mypy src tests labs

# 4. Launch Claude Code
claude
```

Inside Claude Code:
- `/start-lab 01` — Scaffolds hypothesis, requires your prediction, and sets up the active lab.
- `/drill` — Injects intentional chaos, hidden harness defects, or adversarial payloads.
- `/ladder` — Runs the Evidence Ladder against the active lab (ruff, mypy, pytest, gate.py).
- `/audit` — Fresh read-only reviewer checks uncommitted changes against CLAUDE.md invariants.
- `/defend 01` — Conducts a 5-question oral architectural defense to qualify for `MASTERED` status.
