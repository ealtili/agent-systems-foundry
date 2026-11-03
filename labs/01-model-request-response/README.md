# Lab 01: Model Request-Response & Structured Output

**Track A · Mode A (Guided) · Est. 4-6 h · Live-API budget: needs your explicit approval (see Step 6)**

## Systems context
A model returns *probabilistic text*; your program needs *typed values*. Every agent loop in this course crosses that boundary thousands of times. This lab measures the boundary instead of trusting it: how often does it break, what does enforcing it cost, and where does each layer (prompt, provider schema, your validator) actually give a guarantee?

## Read first (about 45 min; take notes in `STATE.md`)
Sources marked ✔ were taken from the Claude API skill's source list; the rest I believe exist but did not open: verify before relying on them.
1. ✔ Structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md (`output_config.format`; what a provider-enforced schema does and does not promise)
2. ✔ API errors: https://platform.claude.com/docs/en/api/errors.md (which failures are retryable)
3. ✔ Pricing: https://platform.claude.com/docs/en/about-claude/pricing.md (convert tokens to dollars yourself)
4. Anthropic Python SDK README (github.com/anthropics/anthropic-sdk-python): client `timeout`, `max_retries`, `response.usage`.
5. Anthropic Engineering, "Building effective agents": read only the sections on workflows vs agents.
6. Pydantic v2 docs, "Models" and "Validators": what `model_validate` raises and why.

Questions to answer in `STATE.md` *before* coding (these feed your prediction):
- What does `stop_reason == "max_tokens"` do to a JSON answer?
- With `timeout=T` and `max_retries=R`, what is the worst-case wall-clock of one call?
- If the provider enforces a schema, why do you still need `model_validate`?

## Hypothesis & systems
See `HYPOTHESIS.md`. System A = prompt-only JSON + your own extraction. System B = provider-enforced schema (`output_config.format`) + Pydantic validation at the boundary. Optional middle arm B1 = prompt-only JSON + Pydantic (shows which layer buys what).

Controlled variables (hold constant, record in every log row): model `claude-haiku-5-5`, `max_tokens`, `output_config={"effort": "low"}`, same task prompt text except the format instruction. Do not set `temperature`/`top_p`: non-default sampling values are rejected on this model (Lab 02 covers sampling).

## Task spec
**Domain task:** turn a one-paragraph feature request into a `StructuredPlan` (`src/schema.py`, already given; you may extend it with justification in an ADR note).

Deliverables, in order. Replay and static checks come before any live call.
1. **Contract (STATE.md).** For every case in `fixtures/raw_outputs.jsonl`, decide and write down: success or failure, and the error category you will report. The fixtures are deliberately ambiguous (is prose around a valid object a success?). The contract is your design decision.
2. **`src/client.py::PlanExtractor`.** Implement your contract. Make `tests/test_lab01.py` pass, then add your own tests per fixture case.
3. **`src/runner.py`.** Calls the API for each system, N=20 per system, one JSONL row per call: `system, prompt_version, latency_ms, input_tokens, output_tokens, stop_reason, parse_ok, error_kind`. Explicit `timeout` and `max_retries` on the client; no unbounded call. Add a replay mode that reads recorded rows instead of calling the API, and test against it.
4. **`src/analyze.py`.** Failure rate, token delta, p50/p95 latency per system, from the JSONL only.
5. **Prediction (via `/start-lab 01`).** Written to `STATE.md` before step 6. Commit it before step 6: git history is your evidence that it came first (the gate only checks that both fields are filled).
6. **Live run (needs approval).** 2 systems × 20 calls will exceed the 20k-token threshold in `CLAUDE.md`, so ask first and state the dollar estimate from the pricing page.
7. **Variance analysis in `STATE.md`:** where were you wrong, and why?
8. `/drill`, then `/defend 01`, then `uv run python scripts/gate.py 01-model-request-response`.

## Prompting thread (P1)
Write your extraction prompt as a versioned file (`prompts/extract_v1.txt`). Change exactly one thing for v2 (for example instruction position, or adding one example), rerun the same N, and log `prompt_version`. Question to answer: did the prompt change move the failure rate more than the schema layer did?

## Definition of done (Evidence Ladder)
G1 ruff + mypy strict · G2 pytest incl. your fixture tests · G3 replay of recorded rows reproduces `analyze.py` output · G6 spend under your stated budget · G7 `/defend 01`.

## Fixtures
`fixtures/raw_outputs.jsonl` holds synthetic raw model outputs, hand-written for this lab: not recorded from the API. Real recordings from your live run replace them as the replay source.
