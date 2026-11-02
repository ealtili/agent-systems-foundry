---
paths:
  - "**/*.py"
---

# Python Engineering Invariants

1. **Async Safety & Deadlines:** Every network and external process call must pass an explicit timeout (`timeout=30.0` or `asyncio.timeout`). Never allow unbound socket operations.
2. **Strict Typing:** All functions must have complete type signatures matching `mypy --strict`. Use `Union` syntax `X | Y`, generic aliases `list[str]`, and explicit return types.
3. **No Catch-All Exceptions:** Never write `except Exception: pass`. Catch explicit error types (`APIConnectionError`, `ValidationError`) and preserve causality with `raise ... from err`.
