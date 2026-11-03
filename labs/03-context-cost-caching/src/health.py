"""Cache-health diagnosis. You implement it; tests/test_health.py is the contract."""

from collections.abc import Sequence
from typing import Literal

from src.schema import UsageRow

Verdict = Literal["healthy", "no_caching", "write_only", "intermittent"]


def diagnose(session: Sequence[UsageRow]) -> Verdict:
    """Classify one session's usage rows, given in call order.

    Raises ValueError if fewer than 2 rows (a single call cannot show reuse). Otherwise, in order:
    - "no_caching":   no row has any cache creation and no row has any cache read.
    - "healthy":      every row after the first has cache_read_input_tokens > 0.
    - "write_only":   no row after the first has a cache read (and caching was attempted).
    - "intermittent": anything else (some later rows read, some do not).
    """
    raise NotImplementedError
