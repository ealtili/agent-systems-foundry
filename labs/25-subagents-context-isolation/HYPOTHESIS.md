# Lab 25 Experimental Design

## Control Experiment
- System A (Control): Main agent conducting noisy repository search in root context.
- System B (Experiment): Context-isolated subagents in `.claude/agents/` with restricted tools returning concise structured summaries.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Subagent context isolation prevents root context saturation during deep codebase investigations by >80%.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
