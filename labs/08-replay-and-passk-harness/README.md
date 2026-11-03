# Lab 08: Replay Harness & pass@k Evaluation

**Track:** Track C: Harness Engineering & Control Theory

## Systems Context
The Evidence Ladder demands replayable trajectories (G3) and pass@k reliability (G5) from the first lab. This lab builds the minimal tooling that every later lab relies on; Lab 34 deepens it with OpenTelemetry.

## Objectives
1. Record and deterministically replay a tool-call trajectory.
2. Compute pass@k over N stochastic runs.
3. Execute the A/B control experiment (single run vs pass@k).
4. Defend the design via `/defend`.

## Prompting Thread (P4)
See `CURRICULUM.md`. Version every prompt as a file under `prompts/`, change one variable per run, and log the result in `STATE.md`.

## Spec v2 additions: evaluation rigor
**Read first** (grep headings, do not read whole files): the "Develop tests" page (URL in `REFERENCES.md`), sections "Define your success criteria", "Build evaluations", "Grade your evaluations". Answer in `STATE.md` before coding:
- When is pass^k (all k runs succeed) the right metric and pass@k (at least one of k) the wrong one?
- Name three LLM-judge biases and one experiment that would expose each.
- Why must the final score come from data you never tuned on?

**Deliverables (learner-owned):**
1. Estimators for pass@k and pass^k from n recorded runs, with a test using synthetic outcomes where the two metrics diverge sharply.
2. A dev/test split rule: the test split is scored once per change, and a contamination check flags eval items that overlap prompts or few-shot examples.
3. A judge module: pointwise rubric and pairwise modes. Measure position bias by swapping order, check length effects, and use a judge model different from the generator (record why). Validate against at least 20 labels you wrote yourself and report agreement (for example Cohen's kappa). State where the judge is not trustworthy.
Live judge calls count toward the 20k-token approval threshold in `CLAUDE.md`; replay first.
