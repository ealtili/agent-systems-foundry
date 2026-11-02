# Lab 06 Experimental Design

## Control Experiment
- System A (Control): Monolithic in-process tool binding tightly coupled to the application runtime.
- System B (Experiment): Decoupled Model Context Protocol (MCP) servers communicating over stdio and Streamable HTTP with resource discovery.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Decoupling tools via MCP enables independent testing, security sandboxing, and runtime reuse across Claude Code and external agents.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
