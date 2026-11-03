# Lab 08: Replay Harness & pass@k Evaluation

**Track:** Track C: Harness Engineering & Control Theory

## Systems Context
The Evidence Ladder demands replayable trajectories (G3) and pass@k reliability (G5) from the first lab. This lab builds the minimal tooling that every later lab relies on; Lab 34 deepens it with OpenTelemetry.

## Objectives
1. Record and deterministically replay a tool-call trajectory.
2. Compute pass@k over N stochastic runs.
3. Execute the A/B control experiment (single run vs pass@k).
4. Defend the design via `/defend`.
