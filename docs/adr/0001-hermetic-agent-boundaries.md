# ADR-0001: Hermetic Agent Execution Boundaries

- **Status:** Accepted
- **Date:** 2026-11-03
- **Deciders:** Principal Architect

## Context & Problem Statement
Agents operating with ambient host access frequently inherit unintended environment variables, unpinned configurations, and wide filesystem permissions. This causes silent behavior drift and security vulnerabilities.

## Decision Drivers
- Predictable, deterministic test behavior.
- Defense-in-depth against prompt injection and arbitrary file modification.
- Clear separation between developer workstation CLI usage and headless backend agent runs.

## Decision Outcome
We enforce **Hermetic Agent Boundaries**:
1. Multi-tenant and automated agent harnesses must explicitly specify `setting_sources=[]` when using the Claude Agent SDK.
2. Tools must operate on sandboxed virtual directory paths rather than raw host roots.
3. External environment access must be whitelisted through explicit configuration schemas.

### Positive Consequences
- Zero ambient state leakage between lab runs and multi-tenant sessions.
- Reproducible benchmark trajectories.

### Negative Consequences / Trade-offs
- Filesystem skills must be explicitly registered rather than auto-discovered from user directories.
