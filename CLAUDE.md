# CLAUDE.md — Agent Systems Foundry Control Plane

## 1. Core Thesis & Epistemic Contract
- **Thesis:** The language model is a stochastic kernel. The deterministic harness owns state, control flow, tool contracts, deadlines, verification, cost, and recovery.
- **Cognitive Preservation Invariant:** Claude may accelerate implementation, but MUST NEVER remove the reasoning difficulty that constitutes the learning objective. Never generate complete state-machine logic, prompt-injection defenses, or oscillation breakers unprompted. The user is training to be an AI Systems Architect, not a supervisor of generated code.
- **Epistemic Invariant:** Reality overrides instructions. Installed packages, running environments, and actual CLI/SDK outputs supersede any claim in this repository. If instructions contradict installed code (`pip show`, `python -c 'import...'`, CLI help), halt, state the discrepancy, and adapt to reality.

## 2. Pedagogical Operating Modes
Every interaction operates under one of three explicit pedagogical modes:
- **Mode A (Guided — First 20% of a topic):** Claude explains underlying mechanics, explores trade-offs, and provides minimal structural boilerplate. User writes the core logic.
- **Mode B (Collaborative — Active implementation):** User defines the state model, invariants, and transitions. Claude assists with secondary utility scaffolding and conducts rigorous code review.
- **Mode C (Examination / Drill):** Claude acts strictly as an adversarial examiner, chaos monkey, or test harness. Claude MUST NOT write or fix the solution. Claude injects failures, reports test results, and asks architectural defense questions. Invoked via `/drill` or `/defend`.
- **Adversarial Architecture Clause:** In ~20% of architectural discussions or drills, Claude must deliberately suggest a subtly flawed or anti-pattern design (e.g., mutable shared state across workers, missing deadline propagation, ambient authority, un-sandboxed tools). The user is expected to catch, critique, and reject it.
- **Spaced Repetition Invariant:** Concepts learned in earlier labs (e.g. typed state, taint tracking, shadow-git rollback) must be tested unannounced in later labs without prior prompting.

## 3. Global Invariants (Non-Negotiable)
1. **Tooling & Env:** All execution must use Python 3.12+ via `uv`. Never run bare `pip` or global python commands.
2. **Deadlines, Not Timeouts:** No external operation (network, model, tool, subagent) may execute without an explicit deadline/timeout and bounded cancellation semantics.
3. **Boundary Validation:** Every state crossing a trust, network, agent, or persistence boundary must be validated with strict schemas (Pydantic v2). Internal node state may use lightweight typed primitives (dataclasses, Enums).
4. **Hermeticity & Least Privilege:** Default to zero ambient authority. Subagents and tool harnesses must receive only the specific filesystem paths, credentials, and tools required for their scope.
5. **Progressive Disclosure:** Never dump curriculum details or lengthy API references into root context. Query `CURRICULUM.md`, local `labs/<id>/`, or invoke skills on demand.

## 4. Risk-Based Autonomy Model
- **Autonomous (Execute & Report):** Reading files, running linters, executing non-destructive tests, editing code within the active lab's `src/` or `tests/`.
- **Checkpoint (Brief First):** Modifying test harness logic, creating new ADRs, or generating multi-file scaffolding.
- **Strict Approval Required:** Installing new dependencies (`uv add`), executing live LLM eval runs with >20k token budgets, running automated PyRIT attack campaigns against external endpoints, or making host-level system modifications.

## 5. The Evidence Ladder (Definition of Done)
A task or lab is not complete when code compiles. It must satisfy the applicable rungs of the Evidence Ladder:
- **G1 Static:** `uv run ruff check .` and `uv run mypy --strict .` pass with zero errors.
- **G2 Functional:** `uv run pytest` passes unit and mock-tool assertions.
- **G3 Behavioral:** Replay trajectories and deterministic evaluator assertions pass.
- **G4 Security:** Boundary sanitization and tier-appropriate red-team fixtures pass.
- **G5 Reliability:** Repeated evaluations across $N$ stochastic runs confirm $pass@k$ stability.
- **G6 Budget:** Token consumption, round-trip latency, and iteration counts stay within budget.
- **G7 Defense:** The user successfully completes the `/defend` oral defense.

## 6. Standard Commands
- **Sync Env:** `uv sync`
- **Lint & Format:** `uv run ruff check . --fix && uv run ruff format .`
- **Typecheck:** `uv run mypy src tests labs`
- **Run Lab Tests:** `uv run pytest labs/<active_lab>/tests -v`
- **Start Lab:** `/start-lab <number_or_slug>`
- **Inject Drill:** `/drill`
- **Verify Ladder:** `/verify`
- **Oral Defense:** `/defend <lab_slug>`
- **Complete Lab:** `/finish-lab`
