import pytest
from src.breaker import CircuitBreaker
from src.fakes import FakeClock


def make(threshold: int = 3, reset: float = 30.0) -> tuple[CircuitBreaker, FakeClock]:
    clock = FakeClock()
    return CircuitBreaker(threshold, reset, clock), clock


def state_of(breaker: CircuitBreaker) -> str:
    return breaker.state


def trip(breaker: CircuitBreaker, n: int = 3) -> None:
    for _ in range(n):
        assert breaker.allow()
        breaker.record_failure()


def test_opens_after_consecutive_failures() -> None:
    breaker, _ = make()
    breaker.record_failure()
    breaker.record_failure()
    assert state_of(breaker) == "closed" and breaker.allow()
    breaker.record_failure()
    assert state_of(breaker) == "open" and not breaker.allow()


def test_a_success_resets_the_failure_count() -> None:
    breaker, _ = make()
    for outcome in ["f", "f", "s", "f", "f"]:
        breaker.record_failure() if outcome == "f" else breaker.record_success()
    assert state_of(breaker) == "closed"


def test_stays_open_until_the_reset_time_then_admits_one_trial() -> None:
    breaker, clock = make()
    trip(breaker)
    clock.now = 29.9
    assert not breaker.allow() and state_of(breaker) == "open"
    clock.now = 30.0
    assert breaker.allow() and state_of(breaker) == "half_open"
    assert not breaker.allow()  # the trial is outstanding


def test_state_is_a_pure_read() -> None:
    breaker, clock = make()
    trip(breaker)
    clock.now = 31
    assert state_of(breaker) == "open"
    assert state_of(breaker) == "open"
    assert breaker.allow()
    assert state_of(breaker) == "half_open"


def test_a_successful_trial_closes_the_circuit() -> None:
    breaker, clock = make()
    trip(breaker)
    clock.now = 30
    assert breaker.allow()
    breaker.record_success()
    assert state_of(breaker) == "closed"
    assert breaker.allow() and breaker.allow()


def test_a_failed_trial_reopens_and_restarts_the_timer() -> None:
    breaker, clock = make()
    trip(breaker)
    clock.now = 30
    assert breaker.allow()
    breaker.record_failure()
    assert state_of(breaker) == "open"
    clock.now = 59
    assert not breaker.allow()
    clock.now = 60
    assert breaker.allow()


def test_late_results_while_open_are_ignored() -> None:
    breaker, clock = make()
    trip(breaker)
    clock.now = 1
    breaker.record_success()
    assert state_of(breaker) == "open" and not breaker.allow()
    breaker.record_failure()
    clock.now = 30
    assert breaker.allow()  # the late failure did not restart the timer


def test_bad_configuration_is_rejected() -> None:
    with pytest.raises(ValueError):
        CircuitBreaker(0, 10.0, FakeClock())
    with pytest.raises(ValueError):
        CircuitBreaker(1, -1.0, FakeClock())
