# ADR-0002: Typed Validation at Boundaries vs Lightweight Internal State

- **Status:** Accepted
- **Date:** 2026-11-03
- **Deciders:** Principal Architect

## Context & Problem Statement
Enforcing heavy runtime validation (e.g. Pydantic v2 `BaseModel`) on every single internal node variable creates computational overhead and awkward syntax for trivial transforms. However, using raw dictionaries everywhere invites runtime `KeyError`s and schema drift.

## Decision Outcome
We establish a two-tier state policy:
1. **Boundary State:** All data entering or exiting an agent, network boundary, tool interface, or persistent store MUST use strict Pydantic models with explicit types and field descriptions.
2. **Internal State:** Internal computation within a single deterministic function or closed graph node may use frozen dataclasses, TypedDicts, or standard Enums.
