# Lab 15: Tree Search Architectures (LATS)

**Track:** Track D: Graphs & Trees

## Systems Context
This laboratory investigates Tree Search Architectures (LATS) from first principles, emphasizing systems trade-offs, boundary invariants, and deterministic failure recovery.

## Objectives
1. Implement the core architectural pattern.
2. Execute the A/B control experiment.
3. Inject chaos and diagnose failures using `/drill`.
4. Defend the design decisions via `/defend`.

## Spec v2 additions: test-time compute at equal budget
**Read first:** write in `STATE.md` the optimization hierarchy you will respect: fix the task definition, then tools and context, then prompts, then workflow, then routing, then training. Say what evidence would justify skipping a level.

**Deliverables (learner-owned):**
1. Compare best-of-N, sequential revision, and your tree search at the **same token budget** on one task family. Plot success vs tokens and state where each wins.
2. A verifier or evaluator for node scoring, with an explicit check for reward hacking (search exploiting a weak scorer).
3. Stretch: search over prompt variants using the Lab 08 harness with a train/validation split; show overfitting to the train split when you let it search too long.
