# Lab 34: Agent Trajectory Evaluations & Observability

**Track:** Track I: Evaluations & Capstone

## Systems Context
This laboratory investigates Agent Trajectory Evaluations & Observability from first principles, emphasizing systems trade-offs, boundary invariants, and deterministic failure recovery.

## Objectives
1. Implement the core architectural pattern.
2. Execute the A/B control experiment.
3. Inject chaos and diagnose failures using `/drill`.
4. Defend the design decisions via `/defend`.

## Spec v2 additions: operating evaluations in production
Builds on the Lab 08 harness.
**Deliverables (learner-owned):**
1. Regression suite wired to headless CI (Lab 29): a prompt, tool or model change must pass the replay set before merge.
2. Online monitoring: alert thresholds on cost per task, p95 latency, failure rate and judge-score drift, computed from OpenTelemetry metrics; one test that fires each alert.
3. Distribution check: compare production-like traces to the eval set and report coverage gaps.
4. Incident drill: a kill switch, a degraded mode (cheaper model or read-only) and a short post-incident note template. Practice one injected incident end to end.
5. Judge calibration at scale: re-validate the Lab 08 judge on fresh human labels and report drift.
