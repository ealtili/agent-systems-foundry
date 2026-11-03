# Planned lab: Managed Agents (the hosted harness)

**Slot:** after Lab 30 (Agent SDK foundations). **Status:** spec only; unnumbered to avoid renumbering. **Facts:** `docs/PLATFORM_FACTS.md` section 5 (re-verify first; this is a beta product).
**Track:** H. **Mode:** B. **Prereqs:** Labs 07 (least privilege), 12 (ledger/resume), 24 (HITL), 30 (surface choice), 34 (evals).
**Extras:** none new. The core `anthropic` package (>= 2.4.0) already exposes `client.beta.agents/environments/sessions`.

## Systems context
Managed Agents is Anthropic running the agent loop *and* hosting the sandbox: you define an agent once, start sessions against an environment, send events and read an event stream. This lab asks what you gain by renting that harness, and what you still must own, by comparing it with the harness you built in Labs 09 to 12.

## Read first (verify links)
- https://platform.claude.com/docs/en/managed-agents/overview and `/quickstart`, plus `/agent-setup`, `/environments`, `/tools`, `/events-and-streaming`, `/scheduled-deployments`, `/self-hosted-sandboxes`, `/choosing-an-environment`.
Questions for `STATE.md`:
- What does the platform own (loop, sandbox, compaction, caching, event persistence) and what do you still own (permissions, evals, cost, data retention)?
- Why are sessions "stateful resources", and what does that imply for zero data retention and HIPAA (not eligible per the overview)?
- When is a self-hosted sandbox the right environment?

## A/B design
A = your own harness (Lab 10 to 12) running the task. B = a Managed Agents session running the same task. Metrics: success on a seeded task fixture, tokens and dollars per solved task, wall-clock, resumability after you kill the client, lines of harness code you own, failure modes you can no longer see.

## Task spec (learner-owned core)
1. Define the agent (system prompt, tools, model) as a versioned file and keep the agent ID; never create agents on the request path.
2. Define an environment with `limited` networking and an explicit `allowed_hosts` list; justify each host (Lab 07). Show web fetch is blocked outside the list.
3. Write the event-stream client: open the stream before sending, handle `agent.message`, `agent.tool_use`, `session.status_idle`, reconnect without duplicating processed events, and enforce your own deadline (Lab 05).
4. Add a permission policy so risky tool calls pause for human approval; connect it to the Lab 24 approval flow. Log every decision.
5. Kill the client mid-run and resume the same session; compare with your Lab 12 crash test.
6. Cost and budget: record usage per session and set a ceiling; compare with Lab 03 caching numbers (reuse your `price_usage` if the usage fields line up; if they do not, say how).
7. One platform feature of your choice at the end (outcomes with a rubric, a scheduled deployment, or a memory store), chosen with a written reason.
8. Delete your sessions when done (transcripts persist until deleted).
Live runs exceed the 20k-token threshold: ask for approval with a dollar estimate.

## Choose dimension
Write the rejection scenario: a case where you would not use Managed Agents (ZDR/HIPAA, tight latency control, custom state machine) and what you would use instead (Lab 30 surface table).

## Prompting thread
Agent system prompt is a versioned file; one change per run, measured on the same fixture.

## Risks
Beta API drift (pin SDK, record date); features in research preview (MCP tunnels, dreaming) need access; cost of long sessions; persistent transcripts holding sensitive data.
