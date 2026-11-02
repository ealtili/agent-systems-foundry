# CURRICULUM.md — Agent Engineering & Systems Track Catalog

Every lab is structured as an experimental hypothesis with a defined baseline, independent variable, measurable metric, and failure modes. Mastery requires reaching **Level 6** (Explain, Build, Debug, Attack, Evaluate, Choose).

### Track A: Model Mechanics & Baseline Control
- **Lab 01: Request-Response Lifecycle & Structured Output:** Raw completions vs. enforced JSON schemas, schema rejection recovery, and latency/cost baselines.
- **Lab 02: Inference Controls & Observable Reasoning Artifacts:** Temperature, thinking effort budgets, isolating structured artifacts (plan, evidence, confidence) from internal reasoning.
- **Lab 03: Context Cost & Prompt Caching Dynamics:** Multi-turn token economics, ephemeral cache breakpoints (`cache_control`), cache eviction mechanics, and cost profiling.

### Track B: Tool Engineering & ACI (Agent-Computer Interface)
- **Lab 04: In-Process Tool Execution & ACI Design:** Tool schema design, parameter ergonomics, type coercion, dynamic registries, and deterministic error reporting.
- **Lab 05: Deadlines, Cancellation & Defensive Dispatch:** Cooperative task cancellation, deadline propagation across tool chains, exponential backoff, and circuit breakers.
- **Lab 06: Model Context Protocol (MCP) Foundations:** Decoupling tools from runtime; building stdio & HTTP/SSE MCP servers, dynamic resources, and client lifecycles.

### Track C: Harness Engineering & Control Theory
- **Lab 07: Compiler-in-the-Loop Backpressure:** AST-aware file patching, capturing LSP/linter/typechecker diagnostics, and injecting targeted feedback into observation state.
- **Lab 08: State Trajectory & The ProgressMonitor Engine:** Detecting exact-state repetition, cyclic oscillation ($S_1 \to S_2 \to S_1$), diagnostic stagnation, and progressive stall recovery policies.
- **Lab 09: Transactional Workspaces & Shadow-Git Checkpoints:** O(1) state rollbacks using shadow git trees, isolating speculative edits, and atomic workspace recovery.
- **Lab 10: Long-Running Harnesses & Context Lifecycle:** Initializer vs. Worker harnesses, sliding-window compaction vs. lossless structured progress ledgers (`STATE.md`).

### Track D: Graphs, Trees & Structural Navigation
- **Lab 11: Control Loops & Dynamic Model Tier Routing:** ReAct, Plan-and-Execute, Reflexion, and dynamic task routing across high-effort reasoning models and low-latency utility models.
- **Lab 12: Tree Search Architectures (LATS):** Language Agent Tree Search with state rollbacks, heuristic state evaluation, and trajectory pruning.
- **Lab 13: Typed Execution Graphs (State Machines & DAGs):** Implementing cyclic graphs with typed reducers, conditional edge routers, and parallel fan-out/fan-in (Map-Reduce).
- **Lab 14: AST Codebase Graphs & Hybrid GraphRAG:** Tree-sitter symbol/call graph indexing, structural dependency traversal, and combining vector similarity with topological graph queries.

### Track E: Distributed Swarms & Coordination
- **Lab 15: Hierarchical Supervisor & Peer Handoff Swarms:** Top-down delegation vs. decentralized peer-to-peer transfers, hop-count livelock breakers, and cycle detection.
- **Lab 16: Shared Blackboard Architectures:** Event-driven pub/sub shared state, optimistic concurrency control (`version_id`), and conflict resolution.
- **Lab 17: Multi-Agent Consensus & Worktree Swarms:** Contract-Net task bidding, Red-vs-Blue-vs-Judge debate, and parallel coding swarms executing across isolated `git worktree` sandboxes.
- **Lab 18: Embodied Computer & Browser Automation:** Headless Playwright integration, accessibility-tree DOM distillation vs. screenshot grounding, and session state persistence.

### Track F: Zero-Trust Security & Adversarial Red Teaming
- **Lab 19: Capability-Based Security & Untrusted Ingestion:** Principle of least privilege, input sanitization, and taint tracking across multi-hop tool calls.
- **Lab 20: Indirect Prompt Injection Defense:** Jailbreak patterns, data exfiltration via canary tokens, and multi-tier defense barriers.
- **Lab 21: Automated Adversarial Testing with Microsoft PyRIT:** Building custom targets, mutation converters, single/multi-turn orchestrators (`Crescendo`, `TreeOfAttacks`), automated scoring, and DuckDB attack ledgers.
- **Lab 22: Human-in-the-Loop (HITL) Checkpoints & Policy Gates:** Cryptographic approval tokens, async suspension/resumption, and policy-driven tool execution firewalls.

### Track G: Claude Code Platform & Extension Engineering
- **Lab 23: Scoped Rules, Slash Commands & Multi-File Refactoring:** YAML `paths:` frontmatter targeting, interactive commands, and atomic multi-file refactoring patterns.
- **Lab 24: Progressive Disclosure Skills (`SKILL.md`):** Authoring skills with frontmatter triggers, executable `scripts/`, lazy-loaded references, and zero idle token overhead.
- **Lab 25: Custom Subagents & Context Isolation:** Designing specialist subagents (`.claude/agents/`), restricting `allowed-tools`, and structured handoff economics.
- **Lab 26: Workspace MCP Orchestration:** Project `.mcp.json`, deferred `ToolSearch`, OAuth 2.1 flows, and `--strict-mcp-config` inheritance isolation.
- **Lab 27: Lifecycle Hooks & Background Monitors:** `PreToolUse`, `PostToolUse`, and `Stop` hooks in `settings.json`, dynamic input rewriting, and background log monitors.
- **Lab 28: Distributable Plugins & Headless CI:** Packaging plugins (`.claude-plugin/`), LSP integration, and headless evaluation pipelines using `claude -p --output-format stream-json`.

### Track H: Claude Agent SDK & Runtime Sandboxing
- **Lab 29: Agent SDK Foundations (`claude-agent-sdk`):** Stateless streaming via `query()`, stateful sessions with `ClaudeSDKClient`, system prompt presets, and session branching.
- **Lab 30: In-Process SDK Tools & Programmatic Subagents:** In-process Python tools via `@tool` and `create_sdk_mcp_server()`, and declaring subagents programmatically via `AgentDefinition`.
- **Lab 31: SDK Permission Pipeline & Dynamic Hooks:** The 6-stage execution pipeline, async `can_use_tool` callbacks, and Python `HookMatcher` interceptors.
- **Lab 32: Hermetic Multi-Tenant Sandboxing:** Setting sources isolation (`setting_sources=[]`), tenant filesystem boundaries, credential scoping, and container deployment.

### Track I: Cross-Runtime Architecture & Evaluations (Capstone)
- **Lab 33: Provider Abstraction & Cross-Runtime Bridge:** Building vendor-neutral agent adapters (`providers/`) to interface Claude Code with external runtimes and shared MCP buses.
- **Lab 34: Agent Trajectory Evaluations & Observability:** OpenTelemetry span instrumentation, deterministic tool replay harnesses, and `pass@k` reliability scoring.
- **Lab 35: Capstone — Zero-Trust Autonomous SWE Agent:** End-to-end production maintainer that ingests issues, maps AST graphs, executes verified worktree fixes, survives PyRIT red-teaming, and opens validated PRs.
