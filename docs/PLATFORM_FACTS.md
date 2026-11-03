# Platform Facts (verified 2026-11-03)

Read from the official pages below on 2026-11-03 through a fetch tool that summarizes each page, so treat quotes as secondary and spot-check the source before building a lab on a detail. These products change quickly: **re-verify before authoring any lab that depends on this file**, and update the date here.

Sources:
- Claude Code, run agents in parallel: https://code.claude.com/docs/en/agents
- Claude Code, dynamic workflows: https://code.claude.com/docs/en/workflows.md
- Claude Agent SDK overview: https://code.claude.com/docs/en/agent-sdk/overview
- Antigravity features: https://antigravity.google/docs/features/
- Antigravity SDK: https://antigravity.google/docs/sdk/overview/ (plus `/docs/sdk/policies`, `/docs/sdk/subagents`)
- Antigravity MCP, enterprise, workflows-to-skills migration: `/docs/mcp`, `/docs/enterprise/`, `/docs/migration/workflows-to-skills/`

## 1. "Dynamic workflows" is overloaded: three different things
| Term | What it is | Where |
| :--- | :--- | :--- |
| **Claude Code dynamic workflows** | A **JavaScript script** that orchestrates many subagents. Claude writes it (or you save one as `/<name>`), a runtime runs it in the background. Intermediate results live in script variables, not Claude's context. | Claude Code CLI, desktop, IDE, `claude -p`, and the Agent SDK |
| Managed Agents multi-agent "workflows" | A `multiagent` config on a server-hosted agent (from the Claude API skill, not re-fetched today). | Claude API / Managed Agents |
| Antigravity "workflows" | Legacy Markdown files, being replaced by Skills (section 3). A separate **Python** `run_workflow` scripting API exists in the SDK (beta; section 4). | Antigravity App/CLI/IDE; SDK |

The course should say which one it means every time.

### Claude Code dynamic workflows, key facts
- Script primitives: `agent()`, `pipeline()`, `parallel()`, `phase()`, `log()`, global `args`; optional `schema` on `agent()` for structured JSON output (validated, up to 5 attempts).
- Runtime limits (default): 16 concurrent agents (configurable 1 to 256), 4,096 items per `parallel()`/`pipeline()`, 1,000 agents per run. No mid-run user input; no filesystem or shell from the script itself (agents do that); no `import()`; `Date.now()`, `Math.random()` and no-arg `new Date()` throw so replay is deterministic.
- Resumable in the same session: completed agents return saved results; the first agent whose prompt differs, and every agent after it, reruns.
- Saved to `.claude/workflows/` (project) or `~/.claude/workflows/`; shareable in plugins; `/workflows` shows progress; built-in `/deep-research`.
- Permissions: launch is approved per permission mode; in `claude -p` and the Agent SDK there is no prompt, so allow `Workflow`/`Workflow(<name>)`, use a hook, `canUseTool`, auto or bypass mode. Subagents obey your permission rules.
- Cost control: size guideline (`small` <5, `medium` <10, `large` <50 agents) is advice, not a cap; "Large workflow" warning above 25 agents or ~1.5M projected tokens. Disable with `disableWorkflows` or `CLAUDE_CODE_DISABLE_WORKFLOWS=1`.
- `ultracode` keyword/effort setting makes Claude plan workflows for substantive tasks; it only triggers on human-stamped input.

### Other Claude Code parallel surfaces (docs page "Run agents in parallel")
Subagents; agent view (`claude agents`, research preview); agent teams (experimental, disabled by default; lead + peers with shared task list); projects (cloud threads, public beta); worktrees; `/batch` skill (5 to 30 worktree-isolated subagents). In every approach the workers are Claude sessions; other tools go in via MCP.

### Claude Agent SDK
Python and TypeScript; "Claude Code as a library"; built-in tools, hooks, subagents, MCP, permissions, sessions, skills/commands/memory loaded from `.claude/`, plugins. The docs' own comparison: Agent SDK vs Claude Code CLI vs Client SDK (tool runner) vs Managed Agents.

## 2. Antigravity facts
- **Surfaces:** App (desktop), CLI (`agy`; App and CLI run the same agent), IDE extensions (VS Code, Visual Studio, JetBrains, Zed, Xcode, Eclipse), SDK. Worktrees are native to Projects (App only).
- **SDK:** Python only. `pip install google-antigravity`; `GEMINI_API_KEY`; `Agent(config)` as `async with`; `LocalAgentConfig`; `agent.chat(...)`; `await response.text()`. Gemini Enterprise via `vertex=True`/project/location. Examples in `google-antigravity/antigravity-sdk-python` under `examples/getting_started/`.
- **SDK capabilities:** personas (`system_instructions`), custom Python tools and built-ins, `SKILL.md` skills, MCP, policies, subagents (static `SubagentConfig` and dynamic self-cloning via `CapabilitiesConfig(enable_subagents=True)`), Pydantic structured output, multimodal input, streamed thoughts, session persistence, hooks, local models (LiteRT or OpenAI-compatible).
- **Policies (SDK):** `deny`, `allow`, `ask_user` from `google.antigravity.hooks.policy`, passed as `LocalAgentConfig(policies=[...])`; `deny("*")` then allow specific tools; `policy.safe_defaults(handler=...)` allows read-only tools and asks for writes and shell. High-risk operations such as `run_command` need an explicit rule.
- **Subagents (SDK):** each has an independent context window; a custom subagent tool must also be in the parent's tool list.
- **MCP:** workspace `<workspace>/.agents/mcp_config.json`; global `~/.gemini/config/mcp_config.json`; stdio and Streamable HTTP in CLI/IDE ("legacy HTTP+SSE ... aren't supported"); MCP Store in App/IDE; CLI `/mcp`; unconfigured MCP tools default to Ask; per-server `enabledTools`/`disabledTools`, `timeoutSeconds` (defaults 300 s connect, 180 s per call).
- **Enterprise:** SSO, BYOID via Workforce Identity Federation, ADC for headless, regional data residency for first-party Gemini models, VPC Service Controls, Private Service Connect, request/response logging to the Google Cloud project, IAM roles, admin opt-in for third-party models.

## 3. Verdicts on claims in the source prompt
| Claim in prompt | Verdict |
| :--- | :--- |
| App, CLI, IDE, Python SDK as surfaces | **Confirmed** |
| `google-antigravity`, `Agent` class, async context manager | **Confirmed** |
| Personas, tools, skills, MCP, policies, subagents (static + self-cloning), structured output, hooks, persistence | **Confirmed** |
| Antigravity Workflows as reusable Markdown sequences | **Outdated.** Legacy workflows (`.agents/workflows/<name>.md`) are being replaced by Skills; the migration page says current workflows "will stop working on October 19, 2026" (before today's date), 12,000-character cap, `/migrate-workflows`. A "new workflows system" is promised but undocumented. Teach Skills; do not build on Markdown workflows. |
| `.agents/mcp_config.json` workspace config | **Confirmed** |
| MCP over stdio, SSE and HTTP | **Partly wrong** for CLI/IDE: stdio and Streamable HTTP only, SSE unsupported. The SDK may differ; verify. |
| Declarative safety policies, interactive approval | **Confirmed** (`deny`/`allow`/`ask_user`, `safe_defaults`) |
| Argument-level predicates; deny-by-default templates | **Confirmed in the installed package (section 4):** `allow/deny/ask_user(tool, when=predicate)`, `deny("*")`, `AutoPolicy`, `safe_defaults`. Not on the docs pages read. |
| Parallel local subagents | **Partly confirmed:** workflow scripts expose `parallel()`/`pipeline()`; tool calls run concurrently via `asyncio.gather`; subagent context isolation confirmed in docs. |
| SSO/BYOID, data residency, VPC-SC | **Confirmed**; "Cloud Logging" is described as logging to the Google Cloud project; admin-enforced tool policies are **not documented**. |
| Claude Agent SDK dynamic workflows | **Confirmed, with correction:** it is a Claude Code feature (JavaScript script, Workflow tool) that the Agent SDK can run; not the same as Managed Agents workflows. |

## 4. Verified from the installed Python packages (2026-11-03)
Installed with `uv sync --group track-h --group track-j`: `claude-agent-sdk` 0.2.176 (bundles Claude Code 2.1.316), `google-antigravity` 0.1.23 (Python >= 3.10). Reality beats docs: these are source-level observations.

**Claude Agent SDK (Python)**
- No Python API to author or start a workflow. The package bundles the Claude Code CLI (`_bundled/claude.exe`), which contains the workflow feature (`disableWorkflows`, `CLAUDE_CODE_DISABLE_WORKFLOWS`, `ultracode`, `workflowSizeGuideline`, a `/workflow-authoring` skill).
- The SDK knows workflow *tasks*: `TaskStarted/Progress/Notification` messages, a `"workflow"` task type with a `name`, `local_workflow` in its deferring task types, and workflow subagent transcripts under `subagents/workflows/<runId>/`. A Python app starts a workflow by prompting, with a `Workflow` allow rule, hook or `can_use_tool`.
- `origin` is stamped on `UserMessage`/`ResultMessage`; the `ultracode` keyword counts only for `{"kind": "human"}`.
- Public docs for the Python page were truncated in the summary; the source is the authority.

**Antigravity SDK (Python)**
- `Agent.run_workflow(workflow=..., script_path=..., description=..., args=...)` (beta) runs a `@workflows.define` function or a `.py` script. Primitives: `phase`, `log`, `agent`, `call_tool`, `parallel`, `pipeline`, `ToolError`, `args`. Scripts are AST-validated (`WorkflowError`). Requires `enable_subagents=True` and `BuiltinTools.RUN_WORKFLOW`. Spawned agents take a workspace mode `inherit`, `branch` (isolated VCS copy, e.g. git worktree) or `share`.
- Policies: `Policy(tool, decision, when=predicate, ask_user=handler, name, reason)`; `Decision` enum includes approve, deny and ask-user; builders `allow`, `deny`, `ask_user`, `allow_all`, `deny_all`; `AutoPolicy` as the safe default; predicates receive the argument dict or a Pydantic model.
- Hooks: `InspectHook`, `DecideHook`, `TransformHook`; concrete hooks `OnSessionStart/End`, `PreTurn`, `PostTurn`, `PreToolCallDecide`, `PostToolCall`, `OnToolError`, `OnInteraction`, `OnCompaction`, `StopHook` (`CONTINUE`/`ALLOW_STOP`).
- Local model connections (LiteRT, OpenAI-compatible) ship in the package.

## 5. Managed Agents (fetched 2026-11-03)
Sources: https://platform.claude.com/docs/en/managed-agents/overview and `/quickstart`. Features marked (skill) come from the Claude API skill and were not re-fetched today.
- **What it is:** a pre-built, configurable agent harness running in Anthropic-managed infrastructure, for long-running and asynchronous work. Status **beta**; header `managed-agents-2026-04-01` (the SDK sets it). Available on the Claude API, Claude Platform on AWS and Claude Models on Google Cloud (Anthropic managed). Supported on all current models.
- **Core concepts:** Agent (model, system prompt, tools, MCP servers, skills; create once, reference by ID), Environment (cloud sandbox, or a self-hosted sandbox on your infrastructure), Session (a running agent instance), Events (user turns, tool results, status updates over SSE; history persisted server-side).
- **Flow in Python:** `client.beta.agents.create(name, model, system, tools=[{"type": "agent_toolset_20260401"}])` -> `client.beta.environments.create(name, config={"type": "cloud", "networking": {"type": "limited", "allow_package_managers": True}})` -> `client.beta.sessions.create(agent=agent.id, environment_id=environment.id, title=...)` -> open `client.beta.sessions.events.stream(session.id)`, then `events.send(session.id, events=[{"type": "user.message", "content": [...]}])`; handle `agent.message`, `agent.tool_use`, `session.status_idle`.
- **Built-in tools:** bash, file operations (read/write/edit/glob/grep), web search and fetch (restricted by `allowed_hosts` under `limited` networking), MCP servers.
- **Declarative CLI:** `ant apply <file>` creates agents/environments from files and records IDs in `claude-lock.json`.
- **Data handling:** sessions are stateful; transcripts persist until you delete them. **Not eligible for zero data retention or HIPAA BAA**, including self-hosted sandboxes.
- **Research preview:** MCP tunnels and "dreaming" need access requests.
- **More features (skill, unverified today):** vaults for credentials, scheduled deployments, outcomes with a grader rubric, multi-agent workflows (`multiagent` config), webhooks, memory stores (separate beta header), permission policies (`always_allow`/`always_ask`/`auto`).
- **Installed SDK check:** `anthropic` 2.4.0 exposes `beta.agents`, `environments`, `sessions` (with `events.stream` and `events.send`), `vaults`, `deployments`, `memory_stores`; `agents.create` accepts `multiagent`, `mcp_servers`, `skills`, `execution_identity`. The repo floor was raised to `anthropic>=2.4.0`.
- **Not to confuse with:** Claude Code dynamic workflows (section 1), the Claude Agent SDK (you host it), or the Tool Runner (a loop helper over the Messages API).

## 6. Keeping this current
Re-fetch the sources above before authoring any lab that depends on them, update the date at the top, and record changed verdicts in git. The Claude docs publish an index at https://code.claude.com/docs/llms.txt.
