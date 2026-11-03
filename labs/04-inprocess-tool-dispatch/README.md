# Lab 04: In-Process Tool Execution & ACI Design

**Track B · Mode A (Guided) · Est. 6-8 h · Live-API budget: needs your explicit approval (see Step 9)**

## Systems context
A tool call is the point where model text becomes an action in your program. Everything between "the model emitted a `tool_use` block" and "your code did something" is harness territory: argument validation, error reporting, ordering of results, and bounding the loop. This lab builds that layer in-process and measures how much the *design of the tool interface* (the agent-computer interface, ACI) changes what the model gets right. It also builds the minimal tool-use loop that Labs 09 and later extend.

## Read first (about 60 min; take notes in `STATE.md`)
Sources marked ✔ come from the Claude API skill's source list or were checked against it (URLs not opened by me); the rest are unverified.
1. ✔ Tool use overview: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview (the `tool_use` / `tool_result` protocol, `tool_choice`, parallel calls, `is_error`)
2. ✔ Structured outputs and strict tool use: https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md (what `strict: true` promises; it needs `additionalProperties: false`)
3. ✔ Handling stop reasons: look up `tool_use`, `max_tokens`, `pause_turn` and `refusal` in the API docs and list what your loop must do for each.
4. Anthropic Engineering, "Writing effective tools for agents" and the ACI section of "Building effective agents" (both exist as far as I know; not opened).
5. Pydantic v2 docs: "Conversion Table" (what lax mode coerces) and "Validation Errors" (the shape of `errors()`).

Facts to keep in mind (from the API skill; verify with a probe where this lab says so):
- Every `tool_result` must reference the `tool_use_id` it answers, and results for one assistant turn go back together in one user message.
- Errors go back as `tool_result` with `is_error: true`, and the model usually adapts.
- `claude-haiku-5-5` accepts a forced `tool_choice`, but a forced call skips thinking. Some newer models (Opus 5.5, Sonnet 5.5, Fable 5.1) reject forced `tool_choice` with a 400. Use `auto` in this lab.
- Replay the assistant's content **unchanged**: editing earlier turns invalidates thinking blocks and the cache (Lab 03).

Questions to answer in `STATE.md` *before* coding (these feed your prediction):
- If the assistant message had two `tool_use` blocks and your reply carries only one `tool_result`, what do you predict the API does? (You will check this with a probe in Step 6.)
- Which failures should the model see (and be able to correct), and which should crash your harness? Where is the line?
- A tool schema is part of the prompt. What does it cost, every turn, and why must it be byte-stable?

## Hypothesis & systems
See `HYPOTHESIS.md`.
- **System A:** one loose tool `run(command: str)`; the model writes `get_order id=1003`, `list_orders customer="Ada Lovelace" status=shipped limit=2`, `refund_order id=1002 amount=500 reason="damaged"`. You parse with a regex or split and return plain-text errors.
- **System B:** three typed tools from `src/tools.py`, schemas generated from Pydantic models by your `Registry`, validated by your `dispatch`, errors in the deterministic format specified in the docstrings.
- **Second experiment (P3):** tool *descriptions* v1 vs v2, scored by first-call selection accuracy on `fixtures/selection_cases.jsonl`.

Controlled variables (record in every row): model `claude-haiku-5-5`, `tool_choice` auto, `max_tokens`, `output_config={"effort": "low"}`, no sampling parameters, same order store fixture, a fresh `OrderStore.from_fixture()` per run.

## Given vs yours
- **Given (passing tests):** `src/schema.py` (argument models, `ToolError`), `src/store.py` (the order store), `src/tools.py` (wiring), and the fixtures.
- **Yours (red until you implement):** `src/registry.py`, `src/dispatch.py`, `src/loop.py`, `src/scoring.py`. Their docstrings are the contract; `tests/` pins them with a scripted fake model, so no API is needed.

## Task spec
Deliverables, in order. Everything through Step 6a is offline.
1. **Contract (STATE.md).** For each failure class (unknown tool, invalid arguments, `ToolError`, handler bug, truncated tool call, unhandled stop reason) write what the model sees and what your harness does. Your table should match the docstrings; if you disagree with one, say why before changing it.
2. **`src/registry.py`.** Registration rules and byte-stable `schemas()`.
3. **`src/dispatch.py`.** `extract_tool_calls`, `dispatch`, `build_result_message`.
4. **`src/loop.py`.** `run_loop`. Write the loop yourself; the fake-model tests will tell you what you got wrong.
5. **`src/scoring.py`.** `selection_correct`.
6. **`src/runner.py`.** Your live runner:
   a. An adapter from an SDK response to `ModelTurn` that preserves what must be replayed. Find out empirically what the API accepts when you replay `model_dump()` output (for example `None` fields) and what it rejects, with the smallest possible live probe, and write the answer in `STATE.md`.
   b. System A's `run(command)` tool and its parser, with your own tests. Its errors are plain strings.
   c. Arms A and B on `fixtures/tasks.jsonl` (8 tasks), 3 runs each, a fresh store per run, grading both the `ANSWER:` line and `final_state` (t5 must change order 1002; t6 must change nothing).
   d. One JSONL row per run: `system, task, run, prompt_version, turns, tool_calls, tool_errors, recovered, success, input_tokens, output_tokens, latency_ms, stop_reason`.
   e. Explicit `timeout` and `max_retries` on the client; `run_loop` gets a `max_turns` and `deadline_s` you can justify.
   f. A replay mode that reads recorded rows.
7. **Protocol probes (needs approval, at most 10 tiny calls).** Predict first, then check each: (a) reply with one `tool_result` when the assistant made two `tool_use` calls; (b) reply with a `tool_use_id` that does not exist. Record the exact status codes and error text.
8. **Prediction (via `/start-lab 04`).** Written to `STATE.md` before Step 9. Commit it before Step 9.
9. **Live run (needs approval).** 2 arms × 8 tasks × 3 runs (about 150 calls), plus selection 12 cases × 2 description versions × 3 runs (72 calls, one call each, nothing executed), plus the probes. This exceeds the 20k-token threshold in `CLAUDE.md`: ask first and state a dollar estimate from the pricing page; my rough guess is a few cents to ten cents on this model, but compute yours.
10. **Variance analysis in `STATE.md`:** where were you wrong? Which arm recovered better from errors, and was it the schema or the error message that did it?
11. `/drill`, then `/defend 04`, then `uv run python scripts/gate.py 04-inprocess-tool-dispatch`.

## Prompting thread (P3)
Tool names, descriptions and parameter docs are prompts. Write `prompts/tools_v1.json` (a `{tool name: description}` map that you pass to `make_registry`). For v2 change exactly one tool's description, rerun the same selection cases, and log the version. Question: did the description change move selection accuracy more than the typed schema did? Remember the two negative cases (s07, s11): a good description also teaches the model when *not* to call.

## Definition of done (Evidence Ladder)
G1 ruff + mypy strict · G2 pytest incl. your own cases (loose-parser tests, adapter tests) · G3 replay reproduces `analyze` output · G4 a handler bug crashes the harness instead of reaching the model (test it) · G6 spend under your stated budget · G7 `/defend 04`.

## Fixtures
- `fixtures/orders.json`: 12 synthetic orders. `tests/test_fixtures.py` proves the task answers from the store, so the ground truth is checked by code.
- `fixtures/tasks.jsonl`: 8 tasks with expected `ANSWER:` and final state.
- `fixtures/selection_cases.jsonl`: 12 first-call cases, 2 of which expect no tool at all.
