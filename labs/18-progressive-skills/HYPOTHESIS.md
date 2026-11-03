# Lab 18 Experimental Design

## Control Experiment
- System A (Control): Embedding procedural instructions in system prompts.
- System B (Experiment): On-demand skills (`SKILL.md`) with frontmatter triggers and lazy-loaded reference documentation.

## Hypothesis & Metrics
- **Independent Variable:** Architectural mechanism under test.
- **Hypothesis:** Progressive disclosure skills reduce idle context consumption to zero until the specific workflow is activated.
- **Dependent Metrics:**
  - Task completion rate (%)
  - Round-trip latency (ms)
  - Token overhead delta (%)
  - Failure recovery rate (%)
