# Lab 12: Long-Running Harnesses & Context Lifecycle

**Track:** Track C: Harness Engineering

## Systems Context
This laboratory investigates Long-Running Harnesses & Context Lifecycle from first principles, emphasizing systems trade-offs, boundary invariants, and deterministic failure recovery.

## Objectives
1. Implement the core architectural pattern.
2. Execute the A/B control experiment.
3. Inject chaos and diagnose failures using `/drill`.
4. Defend the design decisions via `/defend`.

## Spec v2 additions: memory taxonomy and crash-safe resume
**Read first:** write, in `STATE.md`, a table mapping each memory type to a concrete artifact in *this repo*: working (the live context), session (the progress ledger), episodic (replay logs), semantic (docs/ADRs), procedural (skills, rules, CLAUDE.md), team (shared conventions). Say which types your harness will implement and why not the others.

**Deliverables (learner-owned):**
1. A lossless structured progress ledger separate from lossy narrative context. Constraints and approvals live only in the lossless part.
2. A crash test that kills the run after every step k and resumes from the ledger. Prove exactly-once side effects (idempotency keys), not just "it continued".
3. Drift check: restate the goal from the ledger at resume and compare with the original; log a mismatch.
4. Compare compaction vs ledger on a 50-step task: quality, tokens, recovery.
Drill seeds exist in the examiner bank; do not read it.
