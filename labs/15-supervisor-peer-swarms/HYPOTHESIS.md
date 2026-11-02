# Lab 15 Experimental Design

## Control Experiment
- System A (Control): Centralized supervisor bottleneck routing every message through a single node.
- System B (Experiment): Decentralized peer-to-peer handoffs with immutable hop counts, visitor tracking, and cycle breakers.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Peer handoffs with hop-count breakers eliminate supervisor latency bottlenecks while preventing routing livelocks.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
