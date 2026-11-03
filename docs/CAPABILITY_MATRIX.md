# Capability Traceability Matrix

Where each capability is **introduced**, **practiced**, and **applied**, how it is **assessed**, and what it **requires**. Lab numbers follow `CURRICULUM.md`. `tests/test_matrix.py` fails if a referenced lab does not exist, so renumbering cannot silently break this file.

Status: **Covered** (a lab teaches and assesses it) · **Partial** (taught, with a stated hole) · **Planned** (no lab yet; slot proposed).
Capstone = Lab 35 (zero-trust autonomous SWE agent) unless noted.

| Capability | Introduced | Practiced | Applied | Assessment | Prerequisites | Status |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| Tools and tool design | Lab 04 | Lab 04, Lab 31 | Lab 35 | Contract tests; tool-selection accuracy (P3) | Lab 01 | Covered |
| MCPs | Lab 06 | Lab 27 | Lab 35 | Server + client tests; `/defend` | Lab 04 | Covered |
| Skills | Lab 18 | Lab 18, Lab 29 | Lab 35 | Trigger/load tests; zero idle-token check | Lab 17 | Partial (no skill versioning/composition tests) |
| Plugins | Lab 29 | Lab 29 | Lab 35 | Install/uninstall test in headless CI | Lab 18, Lab 28 | Covered |
| Subagents | Lab 19 | Lab 19, Lab 31 | Lab 35 | Context-isolation A/B (tokens, quality) | Lab 07, Lab 17 | Covered |
| Teams of agents | Lab 20 | Lab 20, Lab 21, Lab 22 | Lab 35 | Multi-agent vs single-agent baseline A/B | Lab 19 | Partial (no planner-executor-critic or researcher-writer-reviewer lab) |
| Graph-based workflows | Lab 13 | Lab 14, Lab 15 | Lab 35 | Reducer/router tests; replay | Lab 04 | Covered |
| Dynamic workflows (Claude Code JS scripts driven from Python; Antigravity Python `run_workflow`) | Planned | Planned | Planned | Hand-written workflow vs subagents vs Python orchestration; resume prediction | Lab 13, Lab 19, Lab 20, Lab 31 | **Planned** (spec: `docs/planned_labs/dynamic-workflows.md`; facts verified 2026-11-03 in `docs/PLATFORM_FACTS.md`) |
| Loops and termination | Lab 04 (loop), Lab 10 | Lab 14 | Lab 35 | Oscillation/cycle sabotage drills | Lab 04 | Covered |
| Memory and context engineering | Lab 03 | Lab 12 | Lab 35 | Memory-taxonomy mapping; compaction A/B | Lab 03 | Covered (v2 additions in Lab 12) |
| Long-horizon agents | Lab 12 | Lab 12 | Lab 35 | Crash-at-every-step resume test | Lab 10, Lab 11 | Covered (v2 additions in Lab 12) |
| Model routing | Lab 14 | Lab 14 | Planned | Cost/quality A/B across tiers | Lab 08 | Partial (single vendor only) |
| Multi-vendor models | Planned | Planned | Planned | Same task on two runtimes, measured | Lab 30, Lab 34 | **Planned** (spec: `docs/planned_labs/second-runtime-comparison.md`; Antigravity basics verified, open items listed in the spec) |
| Harnesses | Lab 09 | Lab 10, Lab 11, Lab 12 | Lab 35 | Sabotage drills; `/defend` | Lab 04 | Covered |
| Permissions and safety | Lab 07 | Lab 23, Lab 24, Lab 25, Lab 33 | Lab 35 | Red-team fixtures (G4) | Lab 04 | Covered |
| Human-in-the-loop approval | Lab 24 | Lab 24 | Lab 35 | Suspend/resume + token-forgery tests | Lab 07 | Covered |
| Evaluation and benchmarking | Lab 08 | Lab 34 | Lab 35 | Replay + pass@k; baseline A/B | Lab 04 | Covered |
| LLM-as-judge systems | Lab 08 | Lab 34 | Planned | Judge-vs-human agreement; bias tests | Lab 08 | Covered (v2 additions) |
| Verification | Lab 09 | Lab 15 | Lab 35 | Verifier-gaming drill; generation-verification gap | Lab 09 | Covered (v2 additions) |
| Test-time compute | Lab 15 | Lab 15 | Lab 35 | Best-of-N vs LATS at equal token budget | Lab 08, Lab 09 | Covered (v2 additions) |
| Prompt/context optimization | Lab 02 (P2) | Lab 04 (P3), Lab 08 (P4), Lab 14 (P5), Lab 15 | Lab 35 | Versioned prompts; train/validation split | Lab 02, Lab 08 | Covered (v2 additions in Lab 15) |
| Self-improvement | Lab 14 | Lab 15 | Planned | Bounded revision loop with held-out check | Lab 08, Lab 15 | Partial (no end-to-end bounded self-improvement project) |
| Data for agents | Planned | Planned | Planned | Traces -> eval set -> measured improvement | Lab 08, Lab 34 | **Planned** (data-flywheel lab after Lab 34) |
| Observability | Lab 08 (replay logs) | Lab 34 | Lab 35 | OTel span attributes (`eval-standards` rule) | Lab 08 | Partial (OpenTelemetry arrives at Lab 34; earlier labs use replay logs only) |
| Cost control | Lab 03 | Lab 05, every lab (G6) | Lab 35 | Budget ceilings in tests | Lab 01 | Covered |
| Deployment and operations | Lab 29 | Lab 33, Lab 34 | Lab 35 | Headless CI run; kill-switch/incident drill | Lab 28 | Partial (v2 additions in Lab 34) |
| Choosing a Claude surface | Lab 30 | Lab 30 | Lab 35 | Scenario decision + written defense | Lab 04 | Covered (v2 addition) |
| Hybrid workflow engineering | Planned | Planned | Planned | Document/book workflow with gates | Lab 13, Lab 24 | **Planned** (spec: `docs/planned_labs/hybrid-workflow.md`; book-writing as alternate capstone) |
| Claude Code parallel surfaces (agent teams, agent view, projects, `/batch`) | Planned | Planned | Planned | Choose-the-surface exercise across the five approaches | Lab 19, Lab 22 | **Planned** (only subagents and worktrees are covered today; teams and agent view are experimental/research preview) |
| Skills as the Antigravity extension unit | Planned | Planned | Planned | Port one Claude skill to an Antigravity skill | Lab 18 | **Planned** (Antigravity retired Markdown workflows in favor of skills; see `docs/PLATFORM_FACTS.md`) |

## Planned slots (not yet numbered, to avoid a second renumbering)
1. Hybrid workflow engineering lab, after Lab 13.
2. Data-flywheel lab, after Lab 34.
3. Second-runtime comparison (Claude Agent SDK vs Antigravity SDK on the same task), after Lab 33. Docs verified for the basics on 2026-11-03; remaining open items are listed in its spec.
4. Dynamic workflows (Claude Code), after Lab 31. Term pinned down in `docs/PLATFORM_FACTS.md`.
5. Alternate capstone: AI book-writing workflow.

## How to read the gaps
Specs for the first four slots live in `docs/planned_labs/`. Planned rows are honest zeros, not omissions. Do not claim mastery of a capability whose row says Planned.
