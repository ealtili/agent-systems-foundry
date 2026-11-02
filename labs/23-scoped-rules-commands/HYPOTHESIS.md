# Lab 23 Experimental Design

## Control Experiment
- System A (Control): Monolithic root `CLAUDE.md` loaded into every session context.
- System B (Experiment): Path-scoped `.claude/rules/*.md` loaded selectively via YAML `paths:` globs alongside custom slash commands.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Path-scoped rules eliminate context token waste for unrelated files while guaranteeing rule presence when editing target files.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
