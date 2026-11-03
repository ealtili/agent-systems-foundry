# Lab 05 Experimental Hypothesis & Control Design

## A/B Control Experiment
- **System A (Control):** the SDK's own resilience only: `timeout=1.0`, `max_retries=2`, no outer deadline, no breaker.
- **System B (Experiment):** client `max_retries=0`; `call_with_retry` under a 3 s `Deadline`; `classify_sdk_error`; a `CircuitBreaker` for the burst scenario.

## Experimental Parameters
- **Independent Variable:** who owns the time budget (the SDK's per-attempt knobs vs a propagated deadline) and whether failures are remembered (breaker). Hold the fault scripts, model name, request and clock source constant.
- **Dependent Metrics:**
  - Wall-clock per logical call (s), and whether it stays under the stated bound
  - Endpoint attempts per logical call, and total attempts in `dead_burst`
  - Outcome: `ok` or exception class
  - Calls shed by the breaker
- **Predicted Hypothesis:** *Intentionally blank.* Your prediction and reasoning go in `STATE.md` via `/start-lab`, BEFORE any measurement. No pre-filled numbers. (The earlier draft only said deadlines "bound worst-case time"; this lab makes that a number you must predict and then measure.)
