"""Deadline propagation. You implement it; tests/test_deadline.py is the contract."""

import time
from collections.abc import Callable


class DeadlineExceededError(Exception):
    """The wall-clock budget for the whole operation ran out."""


class Deadline:
    """An absolute point in time on an injectable monotonic clock."""

    def __init__(self, expires_at: float, clock: Callable[[], float]) -> None:
        self.expires_at = expires_at
        self.clock = clock

    @classmethod
    def after(cls, seconds: float, clock: Callable[[], float] = time.monotonic) -> "Deadline":
        """A deadline `seconds` from now. Raises ValueError if seconds < 0."""
        raise NotImplementedError

    def remaining(self) -> float:
        """Seconds left, never negative."""
        raise NotImplementedError

    def expired(self) -> bool:
        """True once the clock has reached expires_at (exactly at expiry counts as expired)."""
        raise NotImplementedError

    def check(self) -> None:
        """Raise DeadlineExceededError if expired, otherwise return."""
        raise NotImplementedError

    def timeout_for(self, cap: float) -> float:
        """The timeout to give one step: min(cap, remaining())."""
        raise NotImplementedError

    def child(self, max_seconds: float, *, reserve: float = 0.0) -> "Deadline":
        """A sub-deadline that can never outlive its parent.

        Expires at min(parent.expires_at - reserve, now + max_seconds) on the SAME clock. The
        reserve is time kept back for cleanup or a final answer. If that is not in the future the
        child is already expired (remaining() == 0, never negative).
        Raises ValueError if max_seconds or reserve is negative.
        """
        raise NotImplementedError
