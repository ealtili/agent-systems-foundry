# Planned lab: Hybrid Workflow Engineering

**Slot:** after Lab 13 (typed execution graphs). **Status:** spec only. **Alternate capstone:** the AI book-writing workflow reuses this lab's skeleton.
**Prereqs:** Labs 05, 08, 11, 12, 13, 24.

## Systems context
Production systems wrap agentic steps in deterministic scaffolding: schemas, validation gates, retries, checkpoints, approvals and recovery. This lab separates *workflow artifacts* (stage list, assignments, validation, approvals, final assembly) from *agentic work* (research synthesis, drafting, review, revision).

## Task (document-processing workflow, learner-owned)
Process a batch of 20 synthetic documents through: intake validation, parallel research workers (bounded), structured extraction, a validation gate, a bounded revision loop, human approval, final assembly.
1. Define each stage's input and output schema (Pydantic) before any model call.
2. Deterministic Python graph owns control flow (Lab 13); agents only fill stages.
3. Idempotent stages with retry, backoff and a dead-letter bucket; checkpoint after each stage; resume after a killed process (reuse the Lab 12 crash test).
4. Human approval gate that can suspend and resume (Lab 24).
5. Termination: max iterations, quality threshold and a cost ceiling per document, all logged with a reason.
6. Failure isolation: one poisoned document must not corrupt the batch.

## A/B
A = one agent run over all documents. B = the hybrid workflow. Metrics: task success, cost per completed document, recovery time after a crash, failures contained, audit trail completeness. Baseline before complexity.

## Constraint inherited from the book capstone
Never generate an entire long artifact in one agent run.

## Prompting thread
Prompt v1 vs v2 for the extraction stage, each tied to an eval (Lab 08).
