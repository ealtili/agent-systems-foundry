"""Backoff arithmetic. You implement it; tests/test_backoff.py is the contract."""

from collections.abc import Callable


def full_jitter_delay(attempt: int, *, base: float, cap: float, rand: Callable[[], float]) -> float:
    """rand() * min(cap, base * 2**attempt), for attempt = 0, 1, 2, ...

    `rand` returns a float in [0, 1]. Raises ValueError if attempt < 0, base <= 0 or cap <= 0.
    """
    raise NotImplementedError


def plan_wait(delay: float, retry_after: float | None, remaining: float) -> float | None:
    """How long to sleep before the next attempt, or None if there is no time to retry.

    The wait is max(delay, retry_after) when the server sent a Retry-After, else delay. If that
    wait is not STRICTLY less than `remaining`, return None: sleeping would spend the whole budget
    and leave nothing for the attempt itself. Raises ValueError for a negative argument.
    """
    raise NotImplementedError
