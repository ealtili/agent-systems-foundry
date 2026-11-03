# Lab 04 Experimental Hypothesis & Control Design

## A/B Control Experiment
- **System A (Control):** one loose tool `run(command: str)`; free-form command string parsed with a regex or `split`; plain-text errors.
- **System B (Experiment):** three typed tools whose JSON schemas come from Pydantic models; arguments validated at the boundary; deterministic error text (`unknown_tool`, `invalid_arguments`, `tool_error`) returned with `is_error`.
- **Second experiment (P3):** tool description v1 vs v2 (one change), measured by first-call selection accuracy.

## Experimental Parameters
- **Independent Variables:** tool interface (loose vs typed) for the task runs; description version for the selection runs. Hold model, effort, store fixture, `tool_choice` and `max_tokens` constant.
- **Dependent Metrics:**
  - Task success: correct `ANSWER:` and correct final store state (%)
  - Tool-error rate: errored results / tool calls (%)
  - Recovery: tasks that succeeded after at least one tool error (%)
  - Tool calls and turns per task; input and output tokens; latency (ms)
  - First-call selection accuracy, including the two "no tool" cases (%)
- **Predicted Hypothesis:** *Intentionally blank.* Your prediction and reasoning go in `STATE.md` via `/start-lab`, BEFORE any measurement. No pre-filled numbers. (An earlier draft promised a ">75% reduction in re-invocations"; that number had no basis and is removed.)
