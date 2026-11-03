import pytest
from src.deadline import Deadline, DeadlineExceededError
from src.fakes import FakeClock


def test_remaining_counts_down_and_never_goes_negative() -> None:
    clock = FakeClock()
    d = Deadline.after(10, clock)
    assert d.remaining() == 10
    clock.now = 4
    assert d.remaining() == 6
    clock.now = 100
    assert d.remaining() == 0.0


def test_exactly_at_expiry_is_expired() -> None:
    clock = FakeClock()
    d = Deadline.after(10, clock)
    clock.now = 9.999
    assert not d.expired()
    clock.now = 10
    assert d.expired()


def test_check_raises_only_when_expired() -> None:
    clock = FakeClock()
    d = Deadline.after(5, clock)
    d.check()
    clock.now = 5
    with pytest.raises(DeadlineExceededError):
        d.check()


def test_timeout_for_is_capped_by_what_is_left() -> None:
    clock = FakeClock()
    d = Deadline.after(10, clock)
    assert d.timeout_for(30) == 10
    assert d.timeout_for(3) == 3
    clock.now = 20
    assert d.timeout_for(3) == 0.0


def test_child_is_capped_by_parent_and_by_max_seconds() -> None:
    clock = FakeClock()
    parent = Deadline.after(10, clock)
    assert parent.child(3).remaining() == 3
    assert parent.child(20).remaining() == 10


def test_child_reserve_keeps_time_back_for_cleanup() -> None:
    clock = FakeClock()
    parent = Deadline.after(10, clock)
    assert parent.child(5, reserve=2).remaining() == 5
    assert parent.child(20, reserve=2).remaining() == 8


def test_child_with_no_time_left_is_already_expired() -> None:
    clock = FakeClock()
    parent = Deadline.after(10, clock)
    child = parent.child(5, reserve=10)
    assert child.remaining() == 0.0
    assert child.expired()


def test_child_shares_the_clock_and_never_outlives_the_parent() -> None:
    clock = FakeClock()
    parent = Deadline.after(10, clock)
    child = parent.child(8)
    clock.now = 4
    assert child.remaining() == 4  # the child's own 8 s, minus 4 elapsed
    clock.now = 9
    assert child.remaining() == 0.0  # expired at 8, while the parent still has 1 s
    assert parent.remaining() == 1


def test_negative_arguments_are_rejected() -> None:
    with pytest.raises(ValueError):
        Deadline.after(-1, FakeClock())
    parent = Deadline.after(10, FakeClock())
    with pytest.raises(ValueError):
        parent.child(-1)
    with pytest.raises(ValueError):
        parent.child(1, reserve=-1)
