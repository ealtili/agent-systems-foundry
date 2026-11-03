"""Circuit breaker. You implement it; tests/test_breaker.py is the contract."""

from collections.abc import Callable
from typing import Literal

State = Literal["closed", "open", "half_open"]


class CircuitBreaker:
    def __init__(
        self, failure_threshold: int, reset_after_s: float, clock: Callable[[], float]
    ) -> None:
        """Raises ValueError if failure_threshold < 1 or reset_after_s < 0."""
        raise NotImplementedError

    @property
    def state(self) -> State:
        """Current state. A pure read: it never changes anything.

        It reports "open" until allow() has admitted the trial call, then "half_open".
        """
        raise NotImplementedError

    def allow(self) -> bool:
        """May a call go to the endpoint now?

        - closed: True.
        - open: False until clock() - opened_at >= reset_after_s. The first allow() after that
          admits exactly ONE trial call (state becomes half_open) and returns True.
        - half_open (trial outstanding): False.
        """
        raise NotImplementedError

    def record_success(self) -> None:
        """closed: reset the consecutive-failure count. half_open: close. open: ignore."""
        raise NotImplementedError

    def record_failure(self) -> None:
        """closed: count; reaching failure_threshold in a row opens it (opened_at = clock()).
        half_open: reopen and restart the timer. open: ignore (a late result)."""
        raise NotImplementedError
