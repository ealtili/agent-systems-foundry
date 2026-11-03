# Planned lab: Second Runtime Comparison (Claude Agent SDK vs Antigravity SDK)

**Slot:** after Lab 33. **Status:** spec only; **blocked until** the open items below are checked. **Facts:** `docs/PLATFORM_FACTS.md` sections 2 and 3.
**Prereqs:** Labs 05, 08, 30, 32, 34. Needs a Gemini API key. The `track-j` dependency group (`google-antigravity`) was approved by the user and added to `pyproject.toml` on 2026-11-03.

## Systems context
Choose a platform from evidence, not brand. Implement the same small task on both Python SDKs, behind a shared tool contract, and compare quality, cost, latency, reliability and developer experience.

## Read first (verify links)
Claude Agent SDK overview; Antigravity SDK overview, policies, subagents, MCP pages (listed in `PLATFORM_FACTS.md`).
Questions for `STATE.md`: How does each SDK express "deny by default, allow reads, ask for writes"? Where does each run its agent loop, and who hosts compute? What happens to tool-call transcripts at the vendor boundary?

## Task (learner-owned adapter and comparison)
1. A vendor-neutral task fixture (fix a seeded failing test in a fixture repo) and a deterministic scorer (the test suite). Reuse the Lab 08 replay and pass@k/pass^k tooling.
2. Two adapters behind one interface: `run(task, deadline) -> Result`. Typed result schema; explicit deadlines on both, using your Lab 05 `Deadline`, because the Anthropic SDK's own timeouts do not bound total wall-clock time (`docs/PLATFORM_FACTS.md` section 6) and the Antigravity SDK's behavior is unverified: probe it first.
3. Equivalent permissions on both, expressed in each SDK's own mechanism (Claude permission rules/hooks; Antigravity `deny`/`allow`/`ask_user` policies). Write the mapping table and name where they cannot be made equivalent.
4. The same MCP server (Streamable HTTP or stdio) connected to both. Note the CLI/IDE do not support SSE.
5. Run N trials each; report pass@k, pass^k, cost per solved task, p50/p95 latency; use a judge from a third model or tests only, never either vendor judging itself.
6. Heterogeneous handoff: Claude plans and Antigravity implements in separate git worktrees (Lab 22), with an explicit handoff schema and a human approval before merge.

## Open items to verify before authoring
- ~~Argument-level predicates and hook decisions~~ resolved 2026-11-03 from the installed package (`when=` predicates, `Decision` enum, hook classes); see `docs/PLATFORM_FACTS.md` section 4.
- How SDK subagent results return to the parent (workflow `parallel()`/`pipeline()` exist; confirm result passing from source or examples).
- Pricing and rate limits for Gemini models used by the SDK.
- Antigravity's replacement for legacy Markdown workflows (promised, undocumented).

## Risks
Vendor API churn (pin versions, record the date), unequal model strength confounding the comparison (compare platforms and model separately where possible), cost (approval for live runs).
