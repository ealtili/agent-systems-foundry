---
paths:
  - "src/foundry/models.py"
  - "labs/**/src/**"
---

# Boundary Validation vs Internal State Rules

1. **Trust Boundaries:** Data originating from LLMs, tools, external APIs, and user inputs must be validated with strict Pydantic v2 schemas (`extra="forbid"` where appropriate).
2. **Internal Node State:** Data existing purely inside a single node or execution thread can use frozen dataclasses or Enums to prevent serialization overhead.
