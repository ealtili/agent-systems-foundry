---
name: defend
description: Conduct a rigorous 5-question oral architectural defense before marking a lab MASTERED.
disable-model-invocation: true
---

# Architectural Defense Protocol (The Path to L6 Mastery)

When invoked via `/defend <lab_slug>`:
1. **Verify Prerequisites:** Inspect `labs/<lab_slug>/STATE.md`. Confirm that G1 Static, G2 Functional, and G3 Behavioral gates are green.
2. **Conduct the 5-Question Oral Defense:** Pose each question one at a time. Wait for the user's answer before asking the next:
   - **Q1 (Mechanism):** What is the exact mechanical invariant this harness/pattern enforces that the raw stochastic model cannot guarantee?
   - **Q2 (Failure Mode):** If we remove component X or introduce network jitter/malformed output, exactly how does the system fail?
   - **Q3 (Trade-off & Cost):** What does this architecture cost in terms of latency, token budget, and implementation complexity compared to a simpler baseline?
   - **Q4 (Attack Vector):** How could an untrusted tool response or indirect prompt injection bypass this specific design?
   - **Q5 (Rejection Scenario):** Describe a concrete production scenario where you would explicitly REJECT this architecture in favor of a simpler or different pattern.
3. **Evaluation:** Evaluate the user's responses candidly:
   - If answers demonstrate deep trade-off comprehension: Award `C (Choose)` and mark `[*]` Mastered in `PROGRESS.md`.
   - If answers are vague or purely descriptive: Mark `[I]` Implemented and provide specific failure scenarios to study.
