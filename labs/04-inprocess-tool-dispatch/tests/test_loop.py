import copy
import json
from collections.abc import Callable
from typing import Any

import pytest
from src.loop import LoopBudgetError, ModelTurn, TruncatedToolCallError, run_loop
from src.registry import Registry, Tool
from src.schema import GetOrderArgs
from src.store import OrderStore
from src.tools import make_registry


class Scripted:
    """A fake model: replays prepared turns and records the history it was shown."""

    def __init__(self, turns: list[ModelTurn], on_call: Callable[[], None] | None = None) -> None:
        self.turns = list(turns)
        self.calls = 0
        self.seen: list[list[dict[str, Any]]] = []
        self.on_call = on_call

    def __call__(self, messages: list[dict[str, Any]]) -> ModelTurn:
        self.seen.append(copy.deepcopy(messages))
        if self.calls >= len(self.turns):
            raise AssertionError("model called more often than scripted")
        turn = self.turns[self.calls]
        self.calls += 1
        if self.on_call:
            self.on_call()
        return turn


class Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def use(tool_id: str, name: str, **args: Any) -> dict[str, Any]:
    return {"type": "tool_use", "id": tool_id, "name": name, "input": args}


def tool_turn(*blocks: dict[str, Any]) -> ModelTurn:
    return ModelTurn(
        content=[{"type": "text", "text": "checking"}, *blocks], stop_reason="tool_use"
    )


def text_turn(text: str) -> ModelTurn:
    return ModelTurn(content=[{"type": "text", "text": text}], stop_reason="end_turn")


def go(
    complete: Scripted,
    registry: Registry | None = None,
    *,
    max_turns: int = 5,
    deadline_s: float = 100.0,
    clock: Callable[[], float] | None = None,
) -> Any:
    reg = registry or make_registry(OrderStore.from_fixture())
    return run_loop(
        complete,
        reg,
        "What is the status of order 1003?",
        max_turns=max_turns,
        deadline_s=deadline_s,
        clock=clock or Clock(),
    )


def test_one_tool_round_trip() -> None:
    first = tool_turn(use("tu_1", "get_order", order_id=1003))
    model = Scripted([first, text_turn("ANSWER: shipped")])
    result = go(model)
    assert result.final_text == "ANSWER: shipped"
    assert (result.turns, result.tool_calls) == (2, 1)
    msgs = result.messages
    assert [m["role"] for m in msgs] == ["user", "assistant", "user", "assistant"]
    assert msgs[0]["content"] == "What is the status of order 1003?"
    assert msgs[1]["content"] == first.content
    block = msgs[2]["content"][0]
    assert block["tool_use_id"] == "tu_1" and "is_error" not in block
    assert json.loads(block["content"])["status"] == "shipped"
    assert len(model.seen[1]) == 3


def test_parallel_calls_are_answered_in_one_message() -> None:
    first = tool_turn(
        use("tu_a", "get_order", order_id=1003), use("tu_b", "get_order", order_id=1004)
    )
    result = go(Scripted([first, text_turn("done")]))
    assert len(result.messages) == 4
    assert [b["tool_use_id"] for b in result.messages[2]["content"]] == ["tu_a", "tu_b"]
    assert result.tool_calls == 2


def test_tool_errors_go_back_to_the_model_and_the_loop_continues() -> None:
    model = Scripted([tool_turn(use("tu_1", "nope")), text_turn("ANSWER: refused")])
    result = go(model)
    assert result.messages[2]["content"][0]["is_error"] is True
    assert result.final_text == "ANSWER: refused"


def test_max_turns_bounds_the_loop() -> None:
    model = Scripted([tool_turn(use("tu", "get_order", order_id=1003))] * 10)
    with pytest.raises(LoopBudgetError):
        go(model, max_turns=3)
    assert model.calls == 3


def test_finishing_exactly_on_the_last_allowed_turn_is_fine() -> None:
    model = Scripted([tool_turn(use("tu", "get_order", order_id=1003)), text_turn("done")])
    assert go(model, max_turns=2).turns == 2


def test_deadline_is_checked_before_every_model_call() -> None:
    clock = Clock()

    def tick() -> None:
        clock.now += 10

    model = Scripted([tool_turn(use("tu", "get_order", order_id=1003))] * 10, on_call=tick)
    with pytest.raises(LoopBudgetError):
        go(model, deadline_s=15.0, max_turns=10, clock=clock)
    assert model.calls == 2


def test_truncated_tool_call_is_never_executed() -> None:
    store = OrderStore.from_fixture()
    cut = ModelTurn(
        content=[use("tu", "refund_order", order_id=1002, amount_cents=500, reason="damaged")],
        stop_reason="max_tokens",
    )
    with pytest.raises(TruncatedToolCallError):
        go(Scripted([cut]), make_registry(store))
    assert store.orders[1002]["refunded_cents"] == 0


def test_unhandled_stop_reasons_are_loud() -> None:
    with pytest.raises(ValueError):
        go(Scripted([ModelTurn(content=[{"type": "text", "text": "x"}], stop_reason="pause_turn")]))
    with pytest.raises(ValueError):
        go(Scripted([ModelTurn(content=[{"type": "text", "text": "x"}], stop_reason="tool_use")]))


def test_a_handler_bug_crashes_the_harness() -> None:
    def boom(_: object) -> str:
        raise KeyError("bug")

    registry = Registry()
    registry.register(Tool("boom", "d", GetOrderArgs, boom))
    with pytest.raises(KeyError):
        go(Scripted([tool_turn(use("tu", "boom", order_id=1))]), registry)
