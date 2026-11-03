"""Bounded concurrent dispatch. You implement it; tests/test_fanout.py is the contract."""

from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import Literal

from src.deadline import Deadline


class ToolCallError(Exception):
    """An expected failure of one call. It becomes data in an Outcome, not an exception."""


@dataclass(frozen=True)
class Outcome:
    index: int
    ok: bool
    value: str | None = None
    error_kind: Literal["error", "timeout"] | None = None
    detail: str | None = None


async def run_all(
    calls: Sequence[Callable[[], Awaitable[str]]],
    deadline: Deadline,
    *,
    concurrency: int,
) -> list[Outcome]:
    """Run the calls concurrently under one deadline and return one Outcome per call, in order.

    - concurrency < 1 raises ValueError. At most `concurrency` calls are in flight; a call waiting
      for a slot has not started.
    - A call that raises ToolCallError becomes Outcome(ok=False, error_kind="error", detail=str(exc)).
      Its siblings are unaffected.
    - When the deadline runs out (or is already expired on entry), every call that has not
      finished is cancelled (never-started ones never start) and reported as
      Outcome(ok=False, error_kind="timeout"). Calls that finished keep their outcome.
    - Any other exception from a call propagates UNCHANGED (not wrapped in an ExceptionGroup)
      after all sibling calls have been cancelled and awaited.
    - If run_all itself is cancelled, every child is cancelled and awaited, then CancelledError
      propagates. No task may outlive run_all.
    """
    raise NotImplementedError
