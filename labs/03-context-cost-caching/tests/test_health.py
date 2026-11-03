import pytest
from src.health import diagnose
from src.schema import UsageRow


def row(*, w5: int = 0, w1: int = 0, read: int = 0) -> UsageRow:
    return UsageRow(
        input_tokens=12,
        output_tokens=45,
        cache_creation_5m_tokens=w5,
        cache_creation_1h_tokens=w1,
        cache_read_input_tokens=read,
    )


def test_healthy_loop_reads_after_first_write() -> None:
    assert diagnose([row(w5=3588), row(w5=128, read=3600), row(w5=128, read=3728)]) == "healthy"


def test_healthy_with_one_hour_writes() -> None:
    assert diagnose([row(w1=3588), row(read=3600)]) == "healthy"


def test_warm_cache_from_before_the_session_is_healthy() -> None:
    assert diagnose([row(read=3600), row(read=3700)]) == "healthy"


def test_no_caching_when_nothing_is_written_or_read() -> None:
    assert diagnose([row(), row(), row()]) == "no_caching"


def test_write_only_means_an_invalidator() -> None:
    assert diagnose([row(w5=3588), row(w5=3716), row(w5=3844)]) == "write_only"


def test_intermittent_when_some_turns_miss() -> None:
    assert diagnose([row(w5=3588), row(read=3600), row(w5=3800)]) == "intermittent"


def test_needs_at_least_two_calls() -> None:
    with pytest.raises(ValueError):
        diagnose([])
    with pytest.raises(ValueError):
        diagnose([row(w5=3588)])
