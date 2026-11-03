"""Cost model. You implement it; tests/test_pricing.py is the contract."""

from dataclasses import dataclass

from src.schema import UsageRow


@dataclass(frozen=True)
class RateCard:
    input_per_mtok: float
    output_per_mtok: float
    cache_read_mult: float = 0.1
    write_5m_mult: float = 1.25
    write_1h_mult: float = 2.0
    max_prompt_tokens: int = 100_000


# Haiku 5.5 short-prompt card. Re-check against the pricing page before a live run.
HAIKU_5_5_SHORT = RateCard(input_per_mtok=0.10, output_per_mtok=0.50)


def price_usage(row: UsageRow, card: RateCard) -> float:
    """Dollar cost of one call.

    Uncached input is billed at the base input rate, cache reads at base * cache_read_mult,
    5-minute writes at base * write_5m_mult, 1-hour writes at base * write_1h_mult, and
    output (thinking included) at the output rate. Rates are per million tokens.

    Raises ValueError if row.prompt_tokens exceeds card.max_prompt_tokens: a longer prompt
    is billed on a different rate card, and pricing it here would be silently wrong.
    """
    raise NotImplementedError


def breakeven_requests(write_mult: float, read_mult: float = 0.1) -> int:
    """Smallest n >= 1 such that caching a prefix is STRICTLY cheaper over n requests.

    Compare in units of one uncached prefix read: cached = write_mult + (n - 1) * read_mult,
    uncached = n. Raises ValueError if read_mult >= 1 (caching can never pay off).
    """
    raise NotImplementedError
