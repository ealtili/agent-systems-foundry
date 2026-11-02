---
name: adr-new
description: Scaffold a new Architectural Decision Record in docs/adr/.
disable-model-invocation: true
---

# New ADR Workflow

When invoked via `/adr-new <title>`:
1. Find the next sequential ADR number in `docs/adr/`.
2. Copy `docs/adr/0000-template.md` to `docs/adr/<number>-<slug>.md`.
3. Populate Context, Decision, Consequences, and Alternatives considered based on user prompt.
