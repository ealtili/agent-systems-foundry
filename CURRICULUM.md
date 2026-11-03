# CURRICULUM.md — Agent Engineering & Systems Track Catalog (ordered)

Capability coverage and planned gaps: `docs/CAPABILITY_MATRIX.md`.

Labs are listed in **study order**; the track tag is a topic label, not a contiguous block. Mastery requires reaching **Level 6** (Explain, Build, Debug, Attack, Evaluate, Choose).

Ordering rationale: capability security (07) and the replay/pass@k harness (08) come before labs that grant agents power; typed graphs (13) precede control loops (14) and tree search (15); Claude Code basics (17-19) precede swarms (20-22); browser use (26) follows prompt-injection defense (23). Old Lab 33 (cross-runtime bridge) was dropped. Study order differs from the original numbering; see git history of this file.

- **Lab 01: Request-Response Lifecycle & Structured Output** `[Track A]` Raw completions vs. enforced JSON schemas, schema rejection recovery, and latency/cost baselines. Every external call carries an explicit timeout from day one. **Prompting thread P1:** versioned extraction prompt; one-variable prompt change vs schema layer.
- **Lab 02: Inference Controls & Observable Reasoning Artifacts** `[Track A]` Effort and adaptive thinking (sampling parameters no longer exist), run-to-run variance, and whether typed artifacts (plan, evidence, confidence) make reasoning observable and confidence calibrated. **Prompting thread P2:** prompt anatomy (role, instructions, examples, output format); A/B one instruction change per run and keep a versioned prompt log.
- **Lab 03: Context Cost & Prompt Caching Dynamics** `[Track A]` Multi-turn token economics, ephemeral cache breakpoints (`cache_control`), cache eviction mechanics, and cost profiling.
- **Lab 04: In-Process Tool Execution & ACI Design** `[Track B]` Tool schema design, parameter ergonomics, type coercion, dynamic registries, and deterministic error reporting. Includes the minimal tool-use loop (model -> tool -> result -> model) that Labs 09+ build on. **Prompting thread P3:** tool name/description/parameter docs are prompts; measure tool-selection accuracy as tool descriptions change.
- **Lab 05: Deadlines, Cancellation & Defensive Dispatch** `[Track B]` Cooperative task cancellation, deadline propagation across tool chains, exponential backoff, and circuit breakers.
- **Lab 06: Model Context Protocol (MCP) Foundations** `[Track B]` Decoupling tools from runtime; building stdio & HTTP/SSE MCP servers, dynamic resources, and client lifecycles.
- **Lab 07: Capability-Based Security & Untrusted Ingestion** `[Track F]` Principle of least privilege, input sanitization, and taint tracking across multi-hop tool calls.
- **Lab 08: Replay Harness & pass@k Evaluation** `[Track C]` Record/replay trajectories and compute pass@k over N runs: the minimal G3/G5 tooling used by all later labs. **Prompting thread P4:** every prompt change ships with an eval; catch a deliberately introduced prompt regression with replay + pass@k. **v2:** pass^k, dev/test split and contamination check, calibrated LLM-as-judge.
- **Lab 09: Compiler-in-the-Loop Backpressure** `[Track C]` AST-aware file patching, capturing LSP/linter/typechecker diagnostics, and injecting targeted feedback into observation state. **v2:** verifier-guided revision and a verifier-gaming detector.
- **Lab 10: State Trajectory & The ProgressMonitor Engine** `[Track C]` Detecting exact-state repetition, cyclic oscillation ($S_1 \to S_2 \to S_1$), diagnostic stagnation, and progressive stall recovery policies.
- **Lab 11: Transactional Workspaces & Shadow-Git Checkpoints** `[Track C]` O(1) state rollbacks using shadow git trees, isolating speculative edits, and atomic workspace recovery.
- **Lab 12: Long-Running Harnesses & Context Lifecycle** `[Track C]` Initializer vs. Worker harnesses, sliding-window compaction vs. lossless structured progress ledgers (`STATE.md`). **v2:** memory taxonomy, lossless ledger vs narrative context, crash-at-every-step resume.
- **Lab 13: Typed Execution Graphs (State Machines & DAGs)** `[Track D]` Implementing cyclic graphs with typed reducers, conditional edge routers, and parallel fan-out/fan-in (Map-Reduce).
- **Lab 14: Control Loops & Dynamic Model Tier Routing** `[Track D]` ReAct, Plan-and-Execute, Reflexion, and dynamic task routing across high-effort reasoning models and low-latency utility models. **Prompting thread P5:** planner/critic/reflection prompts; measure whether a prompt or a control-flow change fixes a failure.
- **Lab 15: Tree Search Architectures (LATS)** `[Track D]` Language Agent Tree Search with state rollbacks, heuristic state evaluation, and trajectory pruning. **v2:** best-of-N vs revision vs tree search at equal token budget; optimization hierarchy.
- **Lab 16: AST Codebase Graphs & Hybrid GraphRAG** `[Track D]` Tree-sitter symbol/call graph indexing, structural dependency traversal, and combining vector similarity with topological graph queries.
- **Lab 17: Scoped Rules, Slash Commands & Multi-File Refactoring** `[Track G]` YAML `paths:` frontmatter targeting, interactive commands, and atomic multi-file refactoring patterns.
- **Lab 18: Progressive Disclosure Skills (`SKILL.md`)** `[Track G]` Authoring skills with frontmatter triggers, executable `scripts/`, lazy-loaded references, and zero idle token overhead.
- **Lab 19: Custom Subagents & Context Isolation** `[Track G]` Designing specialist subagents (`.claude/agents/`), restricting `allowed-tools`, and structured handoff economics.
- **Lab 20: Hierarchical Supervisor & Peer Handoff Swarms** `[Track E]` Top-down delegation vs. decentralized peer-to-peer transfers, hop-count livelock breakers, and cycle detection.
- **Lab 21: Shared Blackboard Architectures** `[Track E]` Event-driven pub/sub shared state, optimistic concurrency control (`version_id`), and conflict resolution.
- **Lab 22: Multi-Agent Consensus & Worktree Swarms** `[Track E]` Contract-Net task bidding, Red-vs-Blue-vs-Judge debate, and parallel coding swarms executing across isolated `git worktree` sandboxes.
- **Lab 23: Indirect Prompt Injection Defense** `[Track F]` Jailbreak patterns, data exfiltration via canary tokens, and multi-tier defense barriers.
- **Lab 24: Human-in-the-Loop (HITL) Checkpoints & Policy Gates** `[Track F]` Cryptographic approval tokens, async suspension/resumption, and policy-driven tool execution firewalls.
- **Lab 25: Automated Adversarial Testing with Microsoft PyRIT** `[Track F]` Building custom targets, mutation converters, single/multi-turn orchestrators (`Crescendo`, `TreeOfAttacks`), automated scoring, and DuckDB attack ledgers.
- **Lab 26: Embodied Computer & Browser Automation** `[Track E]` Headless Playwright integration, accessibility-tree DOM distillation vs. screenshot grounding, and session state persistence.
- **Lab 27: Workspace MCP Orchestration** `[Track G]` Project `.mcp.json`, deferred `ToolSearch`, OAuth 2.1 flows, and `--strict-mcp-config` inheritance isolation.
- **Lab 28: Lifecycle Hooks & Background Monitors** `[Track G]` `PreToolUse`, `PostToolUse`, and `Stop` hooks in `settings.json`, dynamic input rewriting, and background log monitors.
- **Lab 29: Distributable Plugins & Headless CI** `[Track G]` Packaging plugins (`.claude-plugin/`), LSP integration, and headless evaluation pipelines using `claude -p --output-format stream-json`.
- **Lab 30: Agent SDK Foundations (`claude-agent-sdk`)** `[Track H]` Stateless streaming via `query()`, stateful sessions with `ClaudeSDKClient`, system prompt presets, and session branching. **v2:** choose among manual loop, Tool Runner, Managed Agents and Agent SDK for six scenarios.
- **Lab 31: In-Process SDK Tools & Programmatic Subagents** `[Track H]` In-process Python tools via `@tool` and `create_sdk_mcp_server()`, and declaring subagents programmatically via `AgentDefinition`.
- **Lab 32: SDK Permission Pipeline & Dynamic Hooks** `[Track H]` The 6-stage execution pipeline, async `can_use_tool` callbacks, and Python `HookMatcher` interceptors.
- **Lab 33: Hermetic Multi-Tenant Sandboxing** `[Track H]` Setting sources isolation (`setting_sources=[]`), tenant filesystem boundaries, credential scoping, and container deployment.
- **Lab 34: Agent Trajectory Evaluations & Observability** `[Track I]` OpenTelemetry span instrumentation, deterministic tool replay harnesses, and `pass@k` reliability scoring. Deepens the Lab 08 replay/pass@k harness with OpenTelemetry spans. **v2:** CI regression gates, online monitoring and alerts, incident drill, judge re-calibration.
- **Lab 35: Capstone — Zero-Trust Autonomous SWE Agent** `[Track I]` End-to-end production maintainer that ingests issues, maps AST graphs, executes verified worktree fixes, survives PyRIT red-teaming, and opens validated PRs.

**Prompting thread:** P1-P5 above are tracked in `PROGRESS.md`. Rule: no prompt change without a versioned file and a measurement.
