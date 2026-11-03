# Lab 16 Experimental Design

## Control Experiment
- System A (Control): Lexical grep/glob search across source files.
- System B (Experiment): Tree-sitter AST symbol and call-graph indexing combined with topological dependency traversal.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Structural AST graph traversal reduces irrelevant file reads by >60% and guarantees discovery of indirect call-chain dependencies.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
