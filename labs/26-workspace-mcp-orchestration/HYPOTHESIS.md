# Lab 26 Experimental Design

## Control Experiment
- System A (Control): Global unpinned MCP configuration in user home directory.
- System B (Experiment): Hermetic project `.mcp.json` with deferred `ToolSearch`, OAuth 2.1 scopes, and `--strict-mcp-config` isolation.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Project-scoped `.mcp.json` guarantees reproducible tool environments across team members and eliminates ambient server leaks.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
