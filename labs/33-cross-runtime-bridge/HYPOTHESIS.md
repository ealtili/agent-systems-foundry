# Lab 33 Experimental Design

## Control Experiment
- System A (Control): Codebase tightly coupled to a single vendor's agent runtime.
- System B (Experiment): Vendor-neutral provider abstraction layer bridging Claude Code and external runtimes over a shared MCP bus.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Provider abstraction decouples agent business logic from specific model providers, ensuring architectural longevity.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
