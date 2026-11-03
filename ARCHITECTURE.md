# ARCHITECTURE.md — Systems Philosophy & Pedagogical Framework

## 1. Core Thesis
> **"The language model is a stochastic kernel. The deterministic harness owns state, control flow, tool contracts, deadlines, verification, cost, and recovery."**

Language models propose probabilistic next tokens; they cannot guarantee type invariants, execution timeouts, or termination conditions. Autonomous agent engineering is the discipline of wrapping stochastic model generation inside deterministic systems software.

```
+-------------------------------------------------------------------------+
|                         Deterministic Harness                           |
|                                                                         |
|   +-------------------+    Tool Execution   +-----------------------+   |
|   |  State Machine    |-------------------->| ACI / Sandboxed Tools |   |
|   |  & ProgressMonitor|                     +-----------------------+   |
|   +-------------------+                                 |               |
|             ^                                           | Observability |
|             | Structured Ingestion                      v & Backpressure|
|   +-------------------+                     +-----------------------+   |
|   | Verification Gate |<--------------------| Compiler / Diagnostics|   |
|   | (Evidence Ladder) |                     +-----------------------+   |
|   +-------------------+                                                 |
|             |                                                           |
|             v Prompt Construction & Budgeting                           |
|   +-----------------------------------------------------------------+   |
|   |                    Stochastic Model Kernel                      |   |
|   |                  (Anthropic Claude Ecosystem)                   |   |
|   +-----------------------------------------------------------------+   |
+-------------------------------------------------------------------------+
```

---

## 2. The 11-Step Learning Loop
Every lab follows an active experimental loop rather than passive code generation:

$$\text{Theory} \to \text{Predict} \to \text{Design} \to \text{Implement} \to \text{Observe} \to \text{Break} \to \text{Repair} \to \text{Attack} \to \text{Measure} \to \text{Compare} \to \text{Defend}$$

1. **Theory:** Understand the systems mechanism and why it exists.
2. **Predict:** State an explicit hypothesis and predicted metric outcome BEFORE executing code.
3. **Design:** Architect the state boundaries, error paths, and invariants.
4. **Implement:** Write the core logic (user writes critical control flow, Claude provides boilerplate).
5. **Observe:** Run the system and capture raw telemetry (latency, token consumption, error rates).
6. **Break:** Deliberately induce failure (timeouts, malformed tool outputs, loops, dropped packets).
7. **Repair:** Engineer deterministic recovery mechanisms and verify healing.
8. **Attack:** Subject the system to adversarial inputs, prompt injection, and taint leaks.
9. **Measure:** Quantify performance against the predicted metrics.
10. **Compare (A/B Testing):** Benchmark System A (without the mechanism) against System B (with the mechanism).
11. **Defend:** Complete the oral architectural defense (`/defend`) answering mechanism, trade-off, and rejection questions.

---

## 3. The 6 Dimensions of Mastery
We measure mastery across six concrete capabilities:
- **Level 1 (Explain):** Explain the mechanism, problem solved, trade-offs, and alternatives.
- **Level 2 (Build):** Implement the pattern from scratch without copying reference code.
- **Level 3 (Debug):** Diagnose and repair deliberate harness sabotage and edge-case failures.
- **Level 4 (Attack):** Subject the component to adversarial inputs and security bypass attempts.
- **Level 5 (Evaluate):** Empirically prove behavior using A/B control experiments and metrics.
- **Level 6 (Choose):** Defend when **NOT** to use this architecture and select superior alternatives.

---

## 4. The Evidence Ladder
A compiling agent is not a correct agent. We verify agent reliability through a progressive ladder:
- **G1 Static:** Type safety (`mypy --strict`) and clean formatting (`ruff`).
- **G2 Functional:** Unit tests verifying tool logic, schema validation, and state transforms.
- **G3 Behavioral:** Recorded trajectory replays (or scripted fakes and injected faults) confirming expected tool-call sequences and recovery loops.
- **G4 Security:** Input sanitization, taint tracking, and canary exfiltration regression tests.
- **G5 Reliability:** Repeated stochastic evaluations over $N$ runs (measuring $pass@k$ and failure modes).
- **G6 Budget:** Ceiling assertions on token usage, latency, and monetary spend.
- **G7 Defense:** Successful completion of the oral architectural defense.

---

## 5. Control Experiments (A/B Comparative Benchmark Design)
Every lab is paired with a control experiment to quantify why the architectural pattern is necessary:
- **Harness Backpressure:** Agent with compiler diagnostics vs. Agent with raw stderr string.
- **Context Isolation:** Parent performing 40-file repo grep vs. Delegating to a scoped subagent.
- **Structural Memory:** Raw keyword search vs. AST symbol call graph traversal.
- **Swarm Concurrency:** Shared working tree edits vs. Isolated `git worktree` sandboxes.
- **Loop Termination:** Naive step counter vs. `ProgressMonitor` with cycle detection.
- **Security Boundaries:** Natural language prompt admonitions vs. Deterministic input sanitization hooks.
- **Prompt Caching:** No cache vs. a breakpoint on the stable prefix, plus a deliberate silent invalidator (a timestamp in the system prompt) to see what a broken cache looks like in the usage fields.
- **Tool Interface:** A loose command string parsed by regex vs. typed tool schemas validated at the boundary, with deterministic model-visible errors.
- **Time Budget:** SDK retries alone vs. a propagated deadline with retries that spend from it and a circuit breaker, under injected faults.

---

## 6. Offline-First Measurement
Replay before live (the `eval-standards` rule) is a design principle, not a convenience:
- **Pure cores:** the learner's logic is written as functions with injectable clocks, sleepers and random sources, so contract tests need no API and no real waiting.
- **Fake models and fault injection:** a scripted fake model exercises the tool loop (Lab 04); a fault-injecting transport under the real SDK exercises retries, `Retry-After` and timeouts offline and for free (Lab 05).
- **Characterization tests:** given tests pin what the platform actually does (SDK retry and timeout behavior, API shapes), so a dependency upgrade fails a test before it changes a result.
- **Live runs are the last rung:** they need approval above the token threshold in `CLAUDE.md`, and each lab states what it spends.

A contract test is only trustworthy once it has passed against a reference implementation. Authored labs are checked that way, with the reference kept out of the repo (see `docs/LAB_TEMPLATE.md`).
