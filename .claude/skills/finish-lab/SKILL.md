---
name: finish-lab
description: Complete the active lab, record takeaways, and advance pointer if /defend passed.
disable-model-invocation: true
---

# Finish Lab Workflow

When the user runs `/finish-lab`:
1. Check whether `/defend` has been completed. If not, prompt the user to run `/defend` first.
2. Review the 6 dimensions in `PROGRESS.md`:
   - E (Explain)
   - B (Build)
   - D (Debug)
   - A (Attack)
   - V (Evaluate)
   - C (Choose)
3. Prompt the user for their final architectural takeaway and record it in `labs/<active_lab>/STATE.md`.
4. Run `uv run python scripts/gate.py <lab> --mark`. Only a passing gate may set `[*]` in `PROGRESS.md`; never edit it by hand.
5. Advance the active pointer in `PROGRESS.md` to the next lab in `CURRICULUM.md`.
6. `gate.py --mark` registers the lab's `concepts.json` cards into the spaced-repetition store automatically.
