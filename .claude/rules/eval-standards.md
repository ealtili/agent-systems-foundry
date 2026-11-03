---
paths:
  - "labs/08*/**"
  - "labs/34*/**"
  - "labs/35*/**"
  - "tests/**"
---

# Evaluation & Observability Standards

1. **Trace Everything:** Tool invocations, model calls, and graph edge transitions must emit OpenTelemetry spans with standardized attributes (`agent.name`, `tool.name`, `tokens.input`, `tokens.output`).
2. **Deterministic Replay:** Tests must verify behavior against recorded trajectory fixtures before invoking live model calls.
