import asyncio
import time
from collections.abc import Awaitable, Callable

import pytest
from src.deadline import Deadline
from src.fanout import Outcome, ToolCallError, run_all

Call = Callable[[], Awaitable[str]]


def after(seconds: float, value: str) -> Call:
    async def call() -> str:
        await asyncio.sleep(seconds)
        return value

    return call


def real_deadline(seconds: float) -> Deadline:
    return Deadline.after(seconds, time.monotonic)


def no_stray_tasks() -> bool:
    return len(asyncio.all_tasks()) == 1  # only the test itself


async def test_outcomes_come_back_in_input_order() -> None:
    calls = [after(0.03, "a"), after(0.01, "b"), after(0.02, "c")]
    outcomes = await run_all(calls, real_deadline(5), concurrency=3)
    assert outcomes == [Outcome(0, True, "a"), Outcome(1, True, "b"), Outcome(2, True, "c")]


async def test_empty_input() -> None:
    assert await run_all([], real_deadline(5), concurrency=2) == []


async def test_a_tool_failure_is_data_and_does_not_hurt_siblings() -> None:
    async def bad() -> str:
        raise ToolCallError("order not found")

    outcomes = await run_all(
        [after(0.01, "a"), bad, after(0.02, "c")], real_deadline(5), concurrency=3
    )
    assert outcomes[0].ok and outcomes[2].ok
    assert outcomes[1] == Outcome(1, False, None, "error", "order not found")


async def test_concurrency_is_bounded() -> None:
    in_flight = 0
    peak = 0

    async def call() -> str:
        nonlocal in_flight, peak
        in_flight += 1
        peak = max(peak, in_flight)
        await asyncio.sleep(0.02)
        in_flight -= 1
        return "x"

    outcomes = await run_all([call] * 6, real_deadline(5), concurrency=2)
    assert all(o.ok for o in outcomes)
    assert peak == 2


async def test_the_deadline_cancels_slow_calls_and_keeps_finished_ones() -> None:
    start = time.monotonic()
    outcomes = await run_all(
        [after(0.0, "fast"), after(10, "slow")], real_deadline(0.15), concurrency=2
    )
    assert time.monotonic() - start < 2.0
    assert outcomes[0] == Outcome(0, True, "fast")
    assert outcomes[1].ok is False and outcomes[1].error_kind == "timeout"
    assert no_stray_tasks()


async def test_calls_waiting_for_a_slot_never_start_after_the_deadline() -> None:
    started: list[int] = []

    def tracked(i: int, seconds: float) -> Call:
        async def call() -> str:
            started.append(i)
            await asyncio.sleep(seconds)
            return "x"

        return call

    outcomes = await run_all([tracked(0, 10), tracked(1, 10)], real_deadline(0.1), concurrency=1)
    assert started == [0]
    assert [o.error_kind for o in outcomes] == ["timeout", "timeout"]
    assert no_stray_tasks()


async def test_an_already_expired_deadline_starts_nothing() -> None:
    started: list[int] = []

    async def call() -> str:
        started.append(1)
        return "x"

    outcomes = await run_all([call, call], real_deadline(0), concurrency=2)
    assert started == []
    assert [o.error_kind for o in outcomes] == ["timeout", "timeout"]


async def test_a_bug_propagates_unwrapped_and_siblings_are_cancelled() -> None:
    cancelled = asyncio.Event()

    async def slow() -> str:
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            cancelled.set()
            raise
        return "x"

    async def bug() -> str:
        await asyncio.sleep(0.01)
        raise KeyError("harness bug")

    with pytest.raises(KeyError):
        await run_all([slow, bug], real_deadline(5), concurrency=2)
    assert cancelled.is_set()
    assert no_stray_tasks()


async def test_cancelling_run_all_cancels_every_child() -> None:
    running = asyncio.Event()
    cancelled: list[int] = []

    def child(i: int) -> Call:
        async def call() -> str:
            running.set()
            try:
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                cancelled.append(i)
                raise
            return "x"

        return call

    task = asyncio.create_task(run_all([child(0), child(1)], real_deadline(30), concurrency=2))
    await running.wait()
    await asyncio.sleep(0.01)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert sorted(cancelled) == [0, 1]
    assert no_stray_tasks()


async def test_bad_concurrency_is_rejected() -> None:
    with pytest.raises(ValueError):
        await run_all([after(0, "x")], real_deadline(5), concurrency=0)
