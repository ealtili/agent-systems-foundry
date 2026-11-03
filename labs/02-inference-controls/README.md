# Lab 02: Inference Controls & Observable Reasoning Artifacts

**Track A · Mode A (Guided) · Est. 4-6 h · Live-API budget: needs your explicit approval (see Step 7)**

## Systems context
Lab 01 measured the boundary between probabilistic text and typed values. This lab asks what you can still *control* on the model side of that boundary, and what you can only *observe*. On current Claude models the classic knobs are gone: `temperature`, `top_p` and `top_k` are rejected (Haiku 5.5 rejects non-default values; API version `2026-10-21` rejects all three on every model). What remains is `effort`, adaptive thinking, `max_tokens`, `stop_sequences` and the prompt itself. You will measure what each one buys, and test a popular belief: that asking a model for "plan, evidence, confidence" in typed fields makes its reasoning observable and its confidence trustworthy.

## Read first (about 45 min; take notes in `STATE.md`)
Sources marked ✔ come from the Claude API skill's source list (URLs not opened by me); the rest are unverified, so check them before relying on them.
1. ✔ Effort: https://platform.claude.com/docs/en/build-with-claude/effort.md (levels, cost-quality trade-off, interaction with thinking)
2. ✔ Adaptive thinking: https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md (what "on by default" means; what `display` controls)
3. ✔ Structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md (re-read the limits from Lab 01)
4. ✔ Pricing: https://platform.claude.com/docs/en/about-claude/pricing.md (thinking tokens are billed as output)
5. Anthropic Python SDK: `response.content` block types, `usage.output_tokens`.
6. Optional: any paper or blog on verbalized confidence calibration in LLMs (search "calibration verbalized confidence LLM"); judge its claims by your own data.

Questions to answer in `STATE.md` *before* coding (these feed your prediction):
- With sampling parameters gone, what are the remaining sources of run-to-run variation, and what could you do to reduce them?
- If thinking text is omitted by default, which field of the response tells you thinking happened and what it cost?
- If the model writes `"confidence": 0.9` in a field, what process produced that number? Is it a probability the model computed, or text it generated?

## Hypothesis & systems
See `HYPOTHESIS.md`.
- **System A:** free-text answer. The prompt asks for reasoning, then a final line `ANSWER: <value>`; your code extracts it.
- **System B:** provider-enforced schema `Verdict` (`src/schema.py`: `answer`, `evidence`, `confidence`), validated by Pydantic.
- **Second variable:** `effort` = `low` vs `high`.
- **Confound to deal with:** A and B differ in two things at once (output format *and* the extra fields). Decide in `STATE.md` whether to add an optional arm **B0** (schema with `answer` only) to separate them, and say what it would tell you.

Controlled variables (record in every log row): model `claude-haiku-5-5`, same question text, same `max_tokens`, no sampling parameters. Check that the effort levels you use are listed for the model in the Models API capabilities before the live run.

## Task spec
Questions are in `fixtures/questions.jsonl` (12, authored with hand-checked answers; one is unanswerable on purpose: the correct answer is `unknown`).

Deliverables, in order. Replay and static checks come before any live call.
1. **Contract (STATE.md).** Decide and write down: what counts as a correct answer (`normalize_answer`), what counts as "the runs agree", and how you will treat an answer of `unknown` on the unanswerable question. These feed the tests.
2. **`src/scoring.py`.** Implement `normalize_answer`, `brier_score`, `calibration_bins`, `agreement_rate` exactly as their docstrings and `tests/test_scoring.py` specify. These are pure functions: write them with the tests, then add your own edge cases.
3. **`src/runner.py`.** Calls the API for each cell of `system × effort`, k=3 runs per question, one JSONL row per call: `question_id, system, effort, run, prompt_version, answer, confidence, correct, latency_ms, input_tokens, output_tokens, stop_reason, content_block_types, error_kind`. Explicit `timeout` and `max_retries`; no unbounded call. Add a replay mode that reads rows instead of calling the API. Grade `correct` with your `normalize_answer`, not with the model.
4. **`src/analyze.py`.** Per system and effort: accuracy, mean output tokens, p50/p95 latency, `agreement_rate`, and for system B the `brier_score` and `calibration_bins`. Test it on `fixtures/recorded_runs.jsonl` (synthetic rows, made up for this lab).
5. **Prediction (via `/start-lab 02`).** Written to `STATE.md` before step 7. Commit it before step 7: git history is your evidence that it came first (the gate only checks that both fields are filled).
6. **Budget estimate.** 12 questions × 2 systems × 2 efforts × 3 runs = 144 calls. Estimate dollars from the pricing page, remembering that billed output includes thinking tokens you cannot see.
7. **Live run (needs approval).** The run exceeds the 20k-token threshold in `CLAUDE.md`: ask first and state your estimate.
8. **Variance analysis in `STATE.md`:** where were you wrong? Is stated confidence calibrated? Does `high` effort pay for itself on the easy questions?
9. `/drill`, then `/defend 02`, then `uv run python scripts/gate.py 02-inference-controls`.

## Prompting thread (P2)
Anatomy of a prompt: role, instructions, examples, output format. Write system A's prompt as `prompts/answer_v1.txt` and system B's as `prompts/verdict_v1.txt`. For v2 change exactly one thing (for example move the format instruction, or add one worked example), rerun the same cells and log `prompt_version`. Question: which moved accuracy more, the prompt change or the effort change?

## Definition of done (Evidence Ladder)
G1 ruff + mypy strict · G2 pytest incl. your edge cases · G3 replay reproduces `analyze.py` output from recorded rows · G6 spend under your stated budget · G7 `/defend 02`.

## Fixtures
- `fixtures/questions.jsonl`: authored questions with hand-verified answers (not model output).
- `fixtures/recorded_runs.jsonl`: **synthetic** result rows, made up for this lab. Your real recordings replace them as the replay source.
