---
paths:
  - "src/foundry/**"
  - "labs/09*/**"
  - "labs/10*/**"
  - "labs/11*/**"
  - "labs/12*/**"
---

# Harness Engineering & ProgressMonitor Rules

1. **Deterministic State Progress:** Every agent execution loop must pass through `ProgressMonitor`.
2. **Cycle & Oscillation Breaking:** If an agent executes identical tool calls or causes identical compilation errors more than twice consecutively, trip an `OscillationError` and force a replan.
3. **Shadow Git Checkpoints:** Mutating actions on files must be preceded by an in-memory shadow git tree snapshot (`ShadowGit`) to guarantee O(1) rollback on verification failure.
