# Reference Reading

Links to the official documentation this course draws on. The pages are Anthropic's, so they are linked here and not copied into the repo. Page contents change often: when a lab depends on a detail, re-read the live page and note the date (see `docs/PLATFORM_FACTS.md` for how platform facts are tracked).

For offline reading, save your own copies in `.local-docs/` (git-ignored).

Not every URL below has been opened. Each authored lab README marks which of its sources were checked (✔) and how; treat the rest as pointers to confirm.

| Page | URL | Used by |
| :--- | :--- | :--- |
| Best practices for Claude Code | https://code.claude.com/docs/en/best-practices | Lab 09 (give Claude a check to run), Labs 17-19, 27-29; the deterministic vs non-deterministic instruction table frames the course thesis |
| Run agents in parallel | https://code.claude.com/docs/en/agents | Lab 19, planned dynamic-workflows lab |
| Dynamic workflows | https://code.claude.com/docs/en/workflows.md | Planned dynamic-workflows lab |
| Agent SDK overview | https://code.claude.com/docs/en/agent-sdk/overview | Labs 30-33 |
| Managed Agents overview | https://platform.claude.com/docs/en/managed-agents/overview | Lab 30, planned Managed Agents lab |
| Prompt engineering overview | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | Prompting thread P1-P5 |
| Claude prompting best practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Lab 02 |
| Prompting Claude Haiku 5.5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5 | Lab 01 (the model it uses) |
| Prompting Claude Sonnet 5.5 / Opus 5.5 / Fable 5.1 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5 (and `-opus-5-5`, `-fable-5-1`) | Lab 14 (model routing) |
| Increase output consistency | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency | Lab 01 |
| Reduce hallucinations | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | Lab 01, Lab 23 |
| Develop tests (define success criteria, build and grade evals) | https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | Lab 08, Lab 34 |
| Structured outputs / API errors / pricing | https://platform.claude.com/docs/en/build-with-claude/structured-outputs.md , https://platform.claude.com/docs/en/api/errors.md , https://platform.claude.com/docs/en/about-claude/pricing.md | Lab 01 |
| Effort parameter / adaptive thinking | https://platform.claude.com/docs/en/build-with-claude/effort.md , https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking.md | Lab 02 |
| Prompt caching / token counting | https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md , https://platform.claude.com/docs/en/build-with-claude/token-counting.md | Lab 03 |
| Tool use overview | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | Lab 04 (and the Agent SDK tool labs 31-32) |
| Python `asyncio`: Coroutines and Tasks (timeouts, TaskGroup, cancellation) | https://docs.python.org/3/library/asyncio-task.html | Lab 05 |
| Exponential Backoff and Jitter (AWS Architecture Blog) | https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/ | Lab 05 |
| CircuitBreaker (Martin Fowler) | https://martinfowler.com/bliki/CircuitBreaker.html | Lab 05 |
| Antigravity docs | https://antigravity.google/docs/features/ , https://antigravity.google/docs/sdk/overview/ | Planned second-runtime lab |
