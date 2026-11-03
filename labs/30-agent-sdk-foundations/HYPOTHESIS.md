# Lab 30 Experimental Design

## Control Experiment
- System A (Control): Spawning external CLI processes and parsing terminal output.
- System B (Experiment): Native Python integration using `claude_agent_sdk` with `query()` streaming and `ClaudeSDKClient` session continuation.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Native SDK integration provides typed message streams, structured result objects, and sub-millisecond process coordination.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
