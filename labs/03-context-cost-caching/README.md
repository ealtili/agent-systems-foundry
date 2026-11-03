# Lab 03: Context Cost & Prompt Caching Dynamics

**Track A · Mode A (Guided) · Est. 4-6 h · Live-API budget: needs your explicit approval (see Step 8)**

## Systems context
An agent loop resends its whole history on every turn, so input cost grows with every step even if each step is small. Prompt caching lets the provider reuse a *prefix* it has already processed. It is cheap when it works and invisible when it fails: a silent invalidator makes every request succeed while the bill stays high, and no error ever tells you. This lab makes the cost visible, builds the instruments that detect a broken cache, and measures what caching actually buys in a multi-turn loop.

## Read first (about 45 min; take notes in `STATE.md`)
Sources marked ✔ come from the Claude API skill's source list (URLs not opened by me) or were checked against the installed SDK; the rest are unverified.
1. ✔ Prompt caching: https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md (prefix match, render order `tools -> system -> messages`, max 4 breakpoints, minimum cacheable prefix, TTLs)
2. ✔ Pricing: https://platform.claude.com/docs/en/about-claude/pricing.md (cache read multiplier, 5-minute vs 1-hour write multipliers, the long-prompt rate card)
3. ✔ Installed SDK 2.4.0 (checked): `messages.create` accepts a top-level `cache_control`, and `usage` carries `cache_creation_input_tokens`, `cache_read_input_tokens` and a `cache_creation` split by TTL.
4. ✔ Token counting: https://platform.claude.com/docs/en/build-with-claude/token-counting.md (measure your prefix before you rely on it)
5. Anthropic Engineering writing on context engineering for agents, if you can find it: read only the parts on caching and long contexts.

Questions to answer in `STATE.md` *before* coding (these feed your prediction):
- Why does a one-byte change early in the prompt invalidate everything after it, and what is the render order that decides "early"?
- `usage.input_tokens` is 12 but the prompt is 3,700 tokens. Where are the rest, and how do you reconstruct the total?
- Why is a 5-minute cache break-even at two requests but a 1-hour cache at three?
- If you edit an earlier turn of the history before replaying it, what happens to the cache?

## Hypothesis & systems
See `HYPOTHESIS.md`. A = no caching. B = an explicit breakpoint on the end of the static system prefix. Optional arms: B2 = top-level automatic caching only; B3 = both (the combination the docs recommend for agent loops). Choose your arms in `STATE.md` and say what each tells you.

Controlled variables (record in every log row): model `claude-haiku-5-5`, the same handbook and the same 10 questions in the same order, `max_tokens`, `output_config={"effort": "low"}`, no sampling parameters. Replay assistant replies back into history **unchanged**.

## The handbook
`fixtures/handbook.md` is a long synthetic document (60 rules, roughly 4-5k tokens by character count) used as the stable prefix. The 10 questions in `fixtures/turns.jsonl` each have a short ground-truth answer, so you can check that caching did not change what the model says.

## Task spec
Deliverables, in order. The pure functions come first and need no API.
1. **Contract (STATE.md).** For `diagnose`, write down in your own words what each verdict means for a real incident (what you would check next for `write_only` versus `no_caching`).
2. **`src/pricing.py`.** Implement `price_usage` and `breakeven_requests`. Both are specified in their docstrings and tested by `tests/test_pricing.py`.
3. **`src/prefix.py`.** Implement `render_blocks` and `first_divergence`: given two requests, find the first block where the cached prefix breaks.
4. **`src/health.py`.** Implement `diagnose` over a session's usage rows.
5. **`src/runner.py`.** Run a 10-turn session per system, one JSONL row per call: `system, session, turn, prompt_version, latency_ms, usage fields, stop_reason, correct`. Build the request so the stable handbook is the prefix and only the question varies. Explicit `timeout` and `max_retries`. Add a replay mode that reads recorded rows. Run `first_divergence` between consecutive requests inside the runner and log the result.
6. **`src/analyze.py`.** Per system: dollars per session (via your `price_usage`), mean latency, accuracy, and `diagnose` per session. Test it on `fixtures/recorded_usage.jsonl` (synthetic rows for three scenarios).
7. **Prediction (via `/start-lab 03`).** Written to `STATE.md` before step 8. Commit it before step 8.
8. **Live run (needs approval).** Count the prefix with the token-counting endpoint first. Plan: 2 to 4 arms × 3 sessions × 10 turns, so 60 to 120 calls. The total exceeds the 20k-token threshold in `CLAUDE.md`, so ask first and state your dollar estimate; my rough guess is a few cents on this model, but compute yours. Decide how you will keep the sessions of one arm from warming each other's cache (a session that starts inside the 5-minute window of the previous one reads, not writes), and justify it.
9. **Sabotage run.** Put `datetime.now()` into the system prompt for one extra session. Predict what `diagnose` says and what the bill does, then check.
10. **Variance analysis in `STATE.md`:** where were you wrong? How much of the saving survived once output tokens are counted?
11. `/drill`, then `/defend 03`, then `uv run python scripts/gate.py 03-context-cost-caching`.

## Prompting thread
No new P-checkpoint here. Practise P2: version the system prompt as `prompts/system_v1.txt` and keep it byte-stable, because in this lab prompt text is also a cache key.

## Definition of done (Evidence Ladder)
G1 ruff + mypy strict · G2 pytest incl. your own cases · G3 replay reproduces `analyze.py` output · G6 spend under your stated budget · G7 `/defend 03`.

## Fixtures
- `fixtures/handbook.md`, `fixtures/turns.jsonl`: authored for this lab (synthetic content, hand-checked answers).
- `fixtures/recorded_usage.jsonl`: **synthetic** usage rows for three scenarios (`uncached`, `cached_ok`, `cached_invalidated`). Your real recordings replace them as the replay source.
