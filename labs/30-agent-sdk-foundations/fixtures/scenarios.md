# Lab 30: surface-choice scenarios

For each scenario pick ONE of: (a) plain Messages API call, (b) manual tool loop, (c) Tool Runner, (d) Managed Agents, (e) Claude Agent SDK. Write the choice and a 3-sentence defense in `STATE.md`: who runs the loop, who hosts the compute, what you give up. Do not look for an answer key; it is examiner-only.

1. Classify 200 support tickets per minute into five labels with a JSON result.
2. A support agent that calls your internal order API from inside your VPC, with a human approval before any refund.
3. Per-customer sessions that need a sandboxed bash and file workspace, run for hours, and you do not want to host the sandboxes.
4. A coding agent over your repository running on your own CI runners that needs file read/edit, grep and shell out of the box.
5. A nightly report generated at 2 a.m. as one deliverable that must meet a written quality bar.
6. A pipeline needing a custom retry/approval state machine with durable checkpoints and no beta dependencies.
