# Lab 09: Compiler-in-the-Loop Backpressure

**Track:** Track C: Harness Engineering

## Systems Context
This laboratory investigates Compiler-in-the-Loop Backpressure from first principles, emphasizing systems trade-offs, boundary invariants, and deterministic failure recovery.

## Objectives
1. Implement the core architectural pattern.
2. Execute the A/B control experiment.
3. Inject chaos and diagnose failures using `/drill`.
4. Defend the design decisions via `/defend`.

## Spec v2 additions: verifier-guided revision
Treat the compiler, linter and type checker as a **verifier** and measure the generation-verification gap.
**Read first:** the Claude Code "Best practices" page (URL in `REFERENCES.md`), section "Give Claude a check to run". Answer in `STATE.md`: why is checking often cheaper or more reliable than generating, and when is it not?

**Deliverables (learner-owned):**
1. Metric: success rate and iterations-to-green for one-shot generation vs revision with structured diagnostics (existing A/B) vs raw stderr.
2. A verifier-gaming detector: the generator must not be able to change what the verifier checks (tests, lint config) or satisfy it by deleting code or adding suppressions. Report a gaming rate as a metric.
3. A hard iteration cap and a termination reason in every log row.
Drill seeds exist in the examiner bank; do not read it.
