# Lab 03 Experimental Hypothesis & Control Design

## A/B Control Experiment
- **System A (Control):** the same 10-turn session with no `cache_control` anywhere.
- **System B (Experiment):** one explicit `cache_control` breakpoint on the last block of the static system prefix.
- **Optional arms:** B2 top-level automatic caching only; B3 explicit prefix breakpoint plus automatic caching for the growing tail.
- **Sabotage arm:** B with a timestamp in the system prompt, to see what a silent invalidator looks like in the metrics.

## Experimental Parameters
- **Independent Variable:** cache configuration (none vs breakpoint placement). Hold model, handbook, questions, `max_tokens` and effort constant.
- **Dependent Metrics:**
  - Dollars per 10-turn session (priced by your own `price_usage`)
  - Cache read share: `cache_read_input_tokens / prompt_tokens` per turn
  - Round-trip latency (ms)
  - Answer accuracy against `fixtures/turns.jsonl` (caching must not change answers)
  - `diagnose` verdict per session
- **Predicted Hypothesis:** *Intentionally blank.* Your prediction and reasoning go in `STATE.md` via `/start-lab`, BEFORE any measurement. No pre-filled numbers. (The earlier draft promised a fixed percentage saving; that number is not evidence. Cache reads are a fraction of the input price, but output tokens are not discounted, so your own data decides the ceiling.)
