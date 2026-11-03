---
name: audit
description: Review uncommitted changes against CLAUDE.md invariants and .claude/rules/ using a fresh read-only reviewer subagent.
disable-model-invocation: true
---

# Audit (invariant review)

When the user runs `/audit`:
1. In this session run `git status --short` and `git diff HEAD` (the reviewer has no shell).
2. Spawn the `reviewer` subagent with that diff and status in its prompt. Ask it to check typed boundaries, missing deadlines, unbounded loops, context bloat, and anything that gives away a learner-owned core (Cognitive Preservation).
3. Relay its BLOCKER / WARNING / PASS list. Do not fix anything unless asked.

For general bug hunting use the built-in `/code-review`; this skill only checks this repo's invariants.
