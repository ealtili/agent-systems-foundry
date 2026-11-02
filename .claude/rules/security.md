---
paths:
  - "labs/19*/**"
  - "labs/20*/**"
  - "labs/21*/**"
  - "labs/22*/**"
---

# Security & PyRIT Red-Teaming Rules

1. **Least Privilege:** Tool definitions must not allow broad shell commands (`bash -c`). Define narrow, parameterized commands.
2. **Taint Tracking:** Untrusted strings fetched from external web sources or tools must be labeled as untrusted before concatenation into prompt context.
3. **PyRIT Memory Isolation:** All PyRIT attack traces must be written to `.pyrit_memory/` and excluded from git.
4. **Canary Guardrails:** High-value data fixtures used in labs must include synthetic canaries (`CANARY_UUID_...`) to verify whether extraction defenses hold.
