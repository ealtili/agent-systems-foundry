import asyncio

import pytest
from src.deadline import Deadline, DeadlineExceededError
from src.fakes import FakeClock
from src.retry import RetriesExhaustedError, RetryableError, RetryPolicy, call_with_retry

POLICY = RetryPolicy(max_attempts=4, attempt_timeout_s=30.0, base_delay_s=1.0, max_delay_s=10.0)


def one() -> float:
    return 1.0


class Script:
    """An op that fails with the given errors in order, then returns 'done'."""

    def __init__(self, *errors: BaseException) -> None:
        self.errors = list(errors)
        self.calls = 0
        self.timeouts: list[float] = []

    async def __call__(self, timeout: float) -> str:
        self.calls += 1
        self.timeouts.append(timeout)
        if self.errors:
            raise self.errors.pop(0)
        return "done"


async def test_success_on_first_try_does_not_sleep() -> None:
    clock, op = FakeClock(), Script()
    result = await call_with_retry(
        op, Deadline.after(100, clock), POLICY, sleep=clock.sleep, rand=one
    )
    assert result == "done"
    assert op.calls == 1 and clock.sleeps == []


async def test_backoff_delays_double_between_attempts() -> None:
    clock, op = FakeClock(), Script(RetryableError("a"), RetryableError("b"))
    await call_with_retry(op, Deadline.after(100, clock), POLICY, sleep=clock.sleep, rand=one)
    assert clock.sleeps == [1.0, 2.0]
    assert op.calls == 3


async def test_exhaustion_chains_the_last_error_and_does_not_sleep_after_it() -> None:
    clock = FakeClock()
    last = RetryableError("last")
    op = Script(RetryableError("1"), RetryableError("2"), RetryableError("3"), last)
    with pytest.raises(RetriesExhaustedError) as info:
        await call_with_retry(op, Deadline.after(100, clock), POLICY, sleep=clock.sleep, rand=one)
    assert info.value.__cause__ is last
    assert op.calls == 4 and len(clock.sleeps) == 3


async def test_non_retryable_errors_propagate_immediately() -> None:
    clock, op = FakeClock(), Script(ValueError("bug"))
    with pytest.raises(ValueError):
        await call_with_retry(op, Deadline.after(100, clock), POLICY, sleep=clock.sleep, rand=one)
    assert op.calls == 1 and clock.sleeps == []


async def test_retry_after_is_honoured_when_it_fits() -> None:
    clock, op = FakeClock(), Script(RetryableError("slow down", retry_after=5.0))
    await call_with_retry(op, Deadline.after(100, clock), POLICY, sleep=clock.sleep, rand=one)
    assert clock.sleeps == [5.0]


async def test_retry_after_longer_than_the_budget_fails_fast() -> None:
    clock = FakeClock()
    cause = RetryableError("slow down", retry_after=5.0)
    op = Script(cause)
    with pytest.raises(DeadlineExceededError) as info:
        await call_with_retry(op, Deadline.after(4, clock), POLICY, sleep=clock.sleep, rand=one)
    assert info.value.__cause__ is cause
    assert op.calls == 1 and clock.sleeps == []


async def test_running_out_of_time_between_attempts_stops_the_loop() -> None:
    clock = FakeClock()
    op = Script(RetryableError("a"), RetryableError("b"), RetryableError("c"))
    with pytest.raises(DeadlineExceededError):
        await call_with_retry(op, Deadline.after(2.5, clock), POLICY, sleep=clock.sleep, rand=one)
    assert clock.sleeps == [1.0]  # the 2.0 s wait would not fit in the 1.5 s left
    assert op.calls == 2


async def test_each_attempt_gets_only_the_time_that_is_left() -> None:
    clock, op = FakeClock(), Script(RetryableError("a"))
    await call_with_retry(op, Deadline.after(10, clock), POLICY, sleep=clock.sleep, rand=one)
    assert op.timeouts == [10.0, 9.0]


async def test_an_attempt_that_exceeds_its_timeout_is_retried() -> None:
    clock = FakeClock()
    calls = 0

    async def op(timeout: float) -> str:
        nonlocal calls
        calls += 1
        if calls == 1:
            await asyncio.sleep(10)
        return "done"

    policy = RetryPolicy(max_attempts=3, attempt_timeout_s=0.05, base_delay_s=1.0, max_delay_s=10.0)
    result = await call_with_retry(
        op, Deadline.after(100, clock), policy, sleep=clock.sleep, rand=one
    )
    assert result == "done" and calls == 2


async def test_cancellation_during_backoff_propagates() -> None:
    clock, op = FakeClock(), Script(RetryableError("a"))
    sleeping = asyncio.Event()

    async def blocked_sleep(seconds: float) -> None:
        sleeping.set()
        await asyncio.Event().wait()

    task = asyncio.create_task(
        call_with_retry(op, Deadline.after(100, clock), POLICY, sleep=blocked_sleep, rand=one)
    )
    await sleeping.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert op.calls == 1


async def test_cancellation_inside_the_operation_is_not_retried() -> None:
    clock = FakeClock()
    started = asyncio.Event()
    calls = 0

    async def op(timeout: float) -> str:
        nonlocal calls
        calls += 1
        started.set()
        await asyncio.Event().wait()
        return "never"

    task = asyncio.create_task(
        call_with_retry(op, Deadline.after(100, clock), POLICY, sleep=clock.sleep, rand=one)
    )
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert calls == 1


async def test_a_single_attempt_policy_never_sleeps() -> None:
    clock, op = FakeClock(), Script(RetryableError("a"))
    policy = RetryPolicy(max_attempts=1, attempt_timeout_s=30.0, base_delay_s=1.0, max_delay_s=10.0)
    with pytest.raises(RetriesExhaustedError):
        await call_with_retry(op, Deadline.after(100, clock), policy, sleep=clock.sleep, rand=one)
    assert clock.sleeps == []
