---
name: ladder
description: Execute the full Evidence Ladder against the active lab.
disable-model-invocation: true
---

# Verify Lab Workflow (Evidence Ladder)

When the user runs `/ladder`:
1. **Gate 1 (Static):** Run `uv run ruff check .` and `uv run mypy --strict labs/<active_lab>`.
2. **Gate 2 (Functional):** Run `uv run pytest labs/<active_lab>/tests -v`.
3. **Gate 3 (Behavioral):** Verify that trajectory fixtures match expected step sequence.
4. **Gate 4 (Security):** Run security fixtures (if applicable).
5. Run `uv run python scripts/gate.py <lab>` (no --mark) and include its PASS/FAIL lines in the scorecard.
