import pytest
from src.backoff import full_jitter_delay, plan_wait


def test_delay_doubles_until_the_cap() -> None:
    top = [full_jitter_delay(i, base=1.0, cap=10.0, rand=lambda: 1.0) for i in range(6)]
    assert top == [1.0, 2.0, 4.0, 8.0, 10.0, 10.0]


def test_jitter_scales_the_delay() -> None:
    assert full_jitter_delay(2, base=1.0, cap=10.0, rand=lambda: 0.5) == 2.0
    assert full_jitter_delay(2, base=1.0, cap=10.0, rand=lambda: 0.0) == 0.0


def test_delay_rejects_bad_input() -> None:
    for kwargs in (
        {"attempt": -1, "base": 1.0, "cap": 1.0},
        {"attempt": 0, "base": 0.0, "cap": 1.0},
        {"attempt": 0, "base": 1.0, "cap": 0.0},
    ):
        with pytest.raises(ValueError):
            full_jitter_delay(rand=lambda: 1.0, **kwargs)  # type: ignore[arg-type]


def test_plan_wait_uses_the_larger_of_delay_and_retry_after() -> None:
    assert plan_wait(1.0, None, 5.0) == 1.0
    assert plan_wait(1.0, 3.0, 5.0) == 3.0
    assert plan_wait(1.0, 0.5, 5.0) == 1.0


def test_plan_wait_gives_up_when_the_wait_would_eat_the_budget() -> None:
    assert plan_wait(1.0, 3.0, 3.0) is None  # equal is not enough: nothing left to attempt with
    assert plan_wait(1.0, 3.0, 2.9) is None
    assert plan_wait(1.0, None, 1.0) is None
    assert plan_wait(1.0, None, 1.1) == 1.0


def test_plan_wait_rejects_negatives() -> None:
    with pytest.raises(ValueError):
        plan_wait(-1.0, None, 5.0)
    with pytest.raises(ValueError):
        plan_wait(1.0, -2.0, 5.0)
    with pytest.raises(ValueError):
        plan_wait(1.0, None, -5.0)
