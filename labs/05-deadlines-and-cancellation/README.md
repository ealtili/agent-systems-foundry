# Lab 05: Deadlines, Cancellation & Defensive Dispatch

**Track B · Mode A (Guided) · Est. 6-8 h · Live-API budget: none. All faults are injected through the real SDK offline, so this lab spends no tokens and needs no approval.**

## Systems context
Lab 04's loop checks its deadline *between* model calls. That is not enough: one hung call, or an SDK quietly sleeping on a `Retry-After` header, can blow straight through it. This lab makes time a first-class resource. A deadline is an absolute point on a monotonic clock that is passed down to every step, retries spend from it instead of multiplying it, cancellation is cooperative and never swallowed, and a circuit breaker stops a dead dependency from eating your budget. You test all of it against the real Anthropic SDK code path with injected failures.

## What I measured before writing this (installed `anthropic` 2.4.0)
These come from probes run while authoring this lab, and from reading the SDK source. `tests/test_faults.py` pins them, so an SDK upgrade that changes any of this will fail a test.
- Defaults: `max_retries=2`, timeout 10 minutes (5 s connect), backoff 0.5 s doubling up to 8 s with jitter.
- Retried: 408, 409, 429, every 5xx, connection errors and timeouts. A response header `x-should-retry` overrides this.
- The SDK obeys `retry-after-ms` / `retry-after` between retries. I found no cap below roughly 49 days in the code. So `timeout` and `max_retries` do **not** bound total wall-clock time.
- With `timeout=0.3` and `max_retries=1` a hung endpoint took 1.21 s, not 0.6 s: two attempts plus backoff.
- An outer `asyncio.timeout(0.5)` cancelled a call configured with `timeout=30, max_retries=2` at exactly 0.5 s.
- The request carries per-phase timeouts (`connect`, `read`, `write`, `pool`): a timeout is not a total deadline.

## Read first (about 60 min; take notes in `STATE.md`)
Sources marked ✔ were checked in this session (probes or SDK source); the rest are unverified.
1. ✔ Anthropic SDK retry behavior: read `_should_retry`, `_calculate_retry_timeout` and `_parse_retry_after_header` in `anthropic/_base_client.py` in your `.venv`, then reproduce the numbers above with `tests/test_faults.py`.
2. ✔ API errors: https://platform.claude.com/docs/en/api/errors.md (which statuses are retryable, what a 429 and a 529 mean).
3. Python docs, "Coroutines and Tasks": `asyncio.timeout`, `TaskGroup`, task cancellation, `asyncio.shield`. Read what `CancelledError` is for and why you must re-raise it.
4. The AWS Architecture Blog post "Exponential Backoff and Jitter" (full jitter vs equal jitter).
5. Martin Fowler's "CircuitBreaker" bliki entry.

Questions to answer in `STATE.md` *before* coding (these feed your prediction):
- For client `timeout=T`, `max_retries=R`, write the worst-case wall-clock of one logical call including backoff, and then again if the server sends `Retry-After: 600`. Which of your numbers did the probes above confirm?
- What does a task owe the event loop when it is cancelled, and what is wrong with `except Exception: pass` and `except BaseException: pass` around an `await`?
- `refund_order` from Lab 04 mutates state. Which operations may be retried automatically, which may not, and what would you need (an idempotency key?) before you could?

## Hypothesis & systems
See `HYPOTHESIS.md`.
- **System A:** the SDK alone: client `timeout=1.0`, `max_retries=2`, no outer deadline.
- **System B:** client `max_retries=0`; your `call_with_retry` under a `Deadline` of 3 s, your `classify_sdk_error`, and (for the burst scenario) your `CircuitBreaker`.

Scenarios (from `src/faults.py`, each a script of what the fake endpoint does on attempt 1, 2, ...):

| name | endpoint behavior |
|---|---|
| `healthy` | answers |
| `flaky` | 500, 500, then answers |
| `rate_limited` | 429 with `retry-after-ms: 2000` on every attempt |
| `slow_recovery` | 429 with `retry-after-ms: 1500`, then answers |
| `hang` | never answers (a read timeout fires after the configured seconds) |
| `dead` | 500 on every attempt |
| `dead_burst` | (a runner scenario) 20 sequential calls against `dead` |

## Given vs yours
- **Given (passing tests):** `src/faults.py` (the fault-injecting transport and `make_client`), `src/fakes.py` (`FakeClock`), and `tests/test_faults.py`, which pins the SDK facts above.
- **Yours (red until you implement):** `src/deadline.py`, `src/backoff.py`, `src/retry.py`, `src/classify.py`, `src/breaker.py`, `src/fanout.py`. Docstrings are the contract; `tests/` pins them with a fake clock (no real sleeping) and short real-time asyncio checks.

## Task spec
Deliverables, in order. Everything is offline.
1. **Contract (STATE.md).** For each of these write what happens and why: an attempt times out; the server sends `Retry-After` longer than the time left; the caller cancels during a backoff sleep; one of ten parallel calls raises a harness bug; the breaker is half-open and the trial call hangs.
2. **`src/deadline.py`.** Absolute deadlines on an injectable clock, child budgets with a cleanup reserve.
3. **`src/backoff.py`.** Full-jitter delay and the "is there time to wait?" decision.
4. **`src/retry.py`.** `call_with_retry`: retries that spend from the deadline, honour `Retry-After` only when it fits, and never swallow cancellation.
5. **`src/classify.py`.** Map SDK exceptions to retryable or not, extracting the server's wait hint.
6. **`src/breaker.py`.** Closed, open, half-open with exactly one trial call.
7. **`src/fanout.py`.** Bounded concurrent dispatch under one deadline with clean cancellation. Decide how you will unwrap `TaskGroup`'s `ExceptionGroup` (or avoid it) so a bug surfaces as itself.
8. **`src/runner.py`.** Run arms A and B on every scenario, 3 runs each, with real clocks and `make_client(...)`. One JSONL row per run: `scenario, arm, run, outcome, wall_s, endpoint_attempts, shed, synthetic=false`. `outcome` is `"ok"` or the exception class name. For B, pass the per-attempt `timeout` into the SDK call and keep `max_retries=0` on the client. Add `dead_burst`: 20 sequential calls, counting how many reached the endpoint (`FaultTransport.attempts`) and how many your breaker shed.
9. **`src/analyze.py`.** Per scenario and arm: median and maximum wall-clock, mean endpoint attempts, outcome counts. Test it against `fixtures/recorded_runs.jsonl` (synthetic rows).
10. **Prediction (via `/start-lab 05`).** Written to `STATE.md` before you run. Commit it first. Predict, for `rate_limited` and `hang`, the wall-clock of each arm, and for `dead_burst` the number of endpoint attempts.
11. **Run the experiment.** About a minute per pass; no API, no cost.
12. **Cancellation test of your own.** Cancel a 10-call fan-out mid-flight and prove no task survives (`asyncio.all_tasks()`), the way `tests/test_fanout.py` does.
13. **Variance analysis in `STATE.md`:** where were you wrong? Was System B's bound a property of your deadline or of your retry count?
14. `/drill`, then `/defend 05`, then `uv run python scripts/gate.py 05-deadlines-and-cancellation`.

## Prompting thread
None in this lab. Carry one habit from Lab 04: anything that goes into a prompt must stay byte-stable, and error text you send back to the model should be short and deterministic.

## Definition of done (Evidence Ladder)
G1 ruff + mypy strict · G2 pytest incl. your own cases · G3 replay reproduces `analyze` output · G4 cancellation leaves no stray tasks and a harness bug is not swallowed (tested) · G6 System B's wall-clock stays under its deadline plus a stated slack in every scenario · G7 `/defend 05`.

## Fixtures
- `fixtures/recorded_runs.jsonl`: **synthetic** result rows (made up for this lab, one per scenario and arm). Your real runs replace them as the replay source.
- The fault scripts themselves are code in `src/faults.py`.
