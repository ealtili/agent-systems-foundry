# Lab 30: Agent SDK Foundations (claude-agent-sdk)

**Track:** Track H: Claude Agent SDK

## Systems Context
This laboratory investigates Agent SDK Foundations (claude-agent-sdk) from first principles, emphasizing systems trade-offs, boundary invariants, and deterministic failure recovery.

## Objectives
1. Implement the core architectural pattern.
2. Execute the A/B control experiment.
3. Inject chaos and diagnose failures using `/drill`.
4. Defend the design decisions via `/defend`.

## Spec v2 additions: choose your Claude surface
**Read first:** the four ways to build an agent on Claude: a manual loop on the Messages API, the Tool Runner (SDK helper over the Messages API), Managed Agents (Anthropic runs the loop and hosts a per-session sandbox), and the Claude Agent SDK (Claude Code as a library; you host it). Key axes: who supplies the loop, who hosts the compute, which tools are built in. Verify against current official docs before relying on any detail; this surface changes quickly. Note the Tool Runner and the Agent SDK are different packages that are easy to confuse.

**Deliverables (learner-owned):**
1. Decide the six scenarios in `fixtures/scenarios.md` and defend each in `STATE.md` (who runs the loop, who hosts compute, what you give up). One scenario deliberately needs no agent.
2. Implement the thinnest vertical slice of the surface you chose for the SDK scenario, with an explicit deadline and permission mode.
3. Rewrite one decision after a constraint changes (for example "no beta dependencies") and say what moved.
