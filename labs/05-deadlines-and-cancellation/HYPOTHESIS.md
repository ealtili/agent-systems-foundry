# Lab 05 Experimental Design

## Control Experiment
- System A (Control): Unbounded asyncio tasks that wait indefinitely on hanging network calls.
- System B (Experiment): Explicit deadline propagation using `asyncio.timeout` with cooperative cancellation tokens and exponential backoff retry circuits.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Explicit deadline propagation prevents agent hanging states and bounds worst-case step execution time deterministically.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
