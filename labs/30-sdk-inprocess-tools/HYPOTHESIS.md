# Lab 30 Experimental Design

## Control Experiment
- System A (Control): Spawning external child processes for every local Python tool via stdio MCP.
- System B (Experiment): In-process `@tool` decorators bundled via `create_sdk_mcp_server()` with programmatic `AgentDefinition` subagents.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** In-process SDK tools eliminate IPC serialization overhead and reduce tool round-trip latency by >85%.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
