# Lab 03 Experimental Design

## Control Experiment
- System A (Control): Sending full multi-turn conversational history on every turn without caching.
- System B (Experiment): Structuring prompts with explicit `cache_control` breakpoints on system instructions and historical tool definitions.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Ephemeral prompt caching achieves >80% cost reduction and 60% latency reduction on multi-turn agent sessions exceeding 10 turns.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
