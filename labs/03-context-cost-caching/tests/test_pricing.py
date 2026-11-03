import pytest
from src.pricing import HAIKU_5_5_SHORT, RateCard, breakeven_requests, price_usage
from src.schema import UsageRow

BIG = RateCard(input_per_mtok=1.0, output_per_mtok=5.0, max_prompt_tokens=10_000_000)


def test_plain_input_and_output() -> None:
    row = UsageRow(input_tokens=1_000_000, output_tokens=100_000)
    assert price_usage(row, BIG) == pytest.approx(1.5)


def test_cache_read_is_a_tenth_of_input() -> None:
    row = UsageRow(input_tokens=0, output_tokens=0, cache_read_input_tokens=2_000_000)
    assert price_usage(row, BIG) == pytest.approx(0.2)


def test_write_premiums_by_ttl() -> None:
    five = UsageRow(input_tokens=0, output_tokens=0, cache_creation_5m_tokens=1_000_000)
    hour = UsageRow(input_tokens=0, output_tokens=0, cache_creation_1h_tokens=500_000)
    assert price_usage(five, BIG) == pytest.approx(1.25)
    assert price_usage(hour, BIG) == pytest.approx(1.0)


def test_haiku_card_mixed_row() -> None:
    row = UsageRow(
        input_tokens=12,
        output_tokens=45,
        cache_read_input_tokens=3600,
        cache_creation_5m_tokens=128,
    )
    assert price_usage(row, HAIKU_5_5_SHORT) == pytest.approx(75.7e-6)


def test_prompt_over_card_limit_is_rejected_not_mispriced() -> None:
    at_limit = UsageRow(input_tokens=100_000, output_tokens=0)
    assert price_usage(at_limit, HAIKU_5_5_SHORT) == pytest.approx(0.01)
    over = UsageRow(input_tokens=60_000, cache_read_input_tokens=40_001, output_tokens=0)
    with pytest.raises(ValueError):
        price_usage(over, HAIKU_5_5_SHORT)


def test_usage_row_rejects_negative_tokens() -> None:
    with pytest.raises(ValueError):
        UsageRow(input_tokens=-1, output_tokens=0)


def test_breakeven_matches_published_multipliers() -> None:
    assert breakeven_requests(1.25) == 2
    assert breakeven_requests(2.0) == 3
    assert breakeven_requests(2.0, read_mult=0.025) == 3


def test_breakeven_is_strict_and_handles_cheap_writes() -> None:
    assert breakeven_requests(1.0) == 2
    assert breakeven_requests(0.9) == 1


def test_breakeven_rejects_useless_cache() -> None:
    with pytest.raises(ValueError):
        breakeven_requests(1.25, read_mult=1.0)
