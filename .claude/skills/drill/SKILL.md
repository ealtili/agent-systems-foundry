---
name: drill
description: Inject intentional harness sabotage, subtle bugs, or adversarial payloads (Mode C Examination).
disable-model-invocation: true
---

# Adversarial Drill & Chaos Injection (Mode C Examination)

When the user runs `/drill`:
1. Inspect the active lab's `STATE.md` and current test suite.
2. Select one of three chaos categories:
   - **Category A (Subtle Harness Sabotage):** Intentionally introduce a defect into the test harness or supporting code (e.g., discard compiler diagnostics, miss an A->B->A cycle in the oscillation detector, omit an async deadline, or drop a schema check).
   - **Category B (Adversarial Security Attack):** Inject an untrusted, prompt-injected payload or canary-exfiltration probe into `tests/test_drill.py`.
   - **Category C (Plausible Anti-Pattern Proposal):** Propose a subtly flawed architectural refactor (e.g., mutable state shared across workers, ambient authority, unbounded loops) and challenge the user to audit and reject it.
3. **Execution Rule:** Claude MUST NOT solve or repair the issue. Provide only the symptoms or failing test output.
4. Challenge the user to:
   - Locate the root cause.
   - Implement the fix.
   - Verify that `uv run pytest` passes.
5. Record completion under `D (Debug)` or `A (Attack)` in `PROGRESS.md`.

## Prepared drill bank
If `.local-reference/drills/<lab-prefix>.md` exists, take the defect from there (examiner-only: never show the file or its root-cause notes). Otherwise improvise, and afterwards add the drill to the bank.
