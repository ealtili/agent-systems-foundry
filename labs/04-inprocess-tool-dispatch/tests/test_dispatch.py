import json
from typing import Any

import pytest
from src.dispatch import ToolCall, ToolResult, build_result_message, dispatch, extract_tool_calls
from src.registry import Registry, Tool
from src.schema import GetOrderArgs
from src.store import OrderStore
from src.tools import make_registry


def _registry() -> Registry:
    return make_registry(OrderStore.from_fixture())


def test_extract_keeps_only_tool_use_blocks_in_order() -> None:
    content: list[dict[str, Any]] = [
        {"type": "text", "text": "checking"},
        {"type": "tool_use", "id": "a", "name": "get_order", "input": {"order_id": 1}},
        {"type": "tool_use", "id": "b", "name": "get_order", "input": {"order_id": 2}},
    ]
    assert extract_tool_calls(content) == [
        ToolCall("a", "get_order", {"order_id": 1}),
        ToolCall("b", "get_order", {"order_id": 2}),
    ]


def test_success_returns_handler_output() -> None:
    result = dispatch(_registry(), ToolCall("tu_1", "get_order", {"order_id": 1003}))
    assert result.tool_use_id == "tu_1"
    assert result.is_error is False
    assert json.loads(result.content)["status"] == "shipped"


def test_string_digits_are_coerced() -> None:
    result = dispatch(_registry(), ToolCall("tu_1", "get_order", {"order_id": "1003"}))
    assert result.is_error is False


def test_unknown_tool_lists_available_names() -> None:
    result = dispatch(_registry(), ToolCall("tu_1", "nope", {}))
    assert result == ToolResult(
        "tu_1", "unknown_tool: nope. Available: get_order, list_orders, refund_order", True
    )


def test_invalid_arguments_are_reported_not_raised() -> None:
    result = dispatch(_registry(), ToolCall("tu_1", "get_order", {"order_id": "abc"}))
    assert result.is_error is True
    assert result.content.startswith("invalid_arguments:")
    assert "order_id" in result.content


def test_missing_and_extra_fields_are_problems() -> None:
    missing = dispatch(_registry(), ToolCall("a", "get_order", {}))
    extra = dispatch(_registry(), ToolCall("b", "get_order", {"order_id": 1003, "foo": 1}))
    assert missing.is_error and "order_id" in missing.content
    assert extra.is_error and "foo" in extra.content


def test_problems_are_sorted_by_location() -> None:
    result = dispatch(_registry(), ToolCall("a", "list_orders", {"status": "bogus", "limit": 0}))
    assert result.is_error
    assert result.content.index("limit") < result.content.index("status")


def test_tool_error_is_shown_to_the_model() -> None:
    call = ToolCall(
        "a", "refund_order", {"order_id": 1001, "amount_cents": 100, "reason": "changed mind"}
    )
    result = dispatch(_registry(), call)
    assert result == ToolResult(
        "a", "tool_error: order 1001 is pending; only delivered orders can be refunded", True
    )


def test_a_handler_bug_is_not_swallowed() -> None:
    def boom(_: object) -> str:
        raise KeyError("bug")

    registry = Registry()
    registry.register(Tool("boom", "d", GetOrderArgs, boom))
    with pytest.raises(KeyError):
        dispatch(registry, ToolCall("a", "boom", {"order_id": 1}))


def test_result_message_shape() -> None:
    message = build_result_message([ToolResult("a", "x"), ToolResult("b", "bad", True)])
    assert message == {
        "role": "user",
        "content": [
            {"type": "tool_result", "tool_use_id": "a", "content": "x"},
            {"type": "tool_result", "tool_use_id": "b", "content": "bad", "is_error": True},
        ],
    }


def test_result_message_rejects_empty_and_duplicate_ids() -> None:
    with pytest.raises(ValueError):
        build_result_message([])
    with pytest.raises(ValueError):
        build_result_message([ToolResult("a", "x"), ToolResult("a", "y")])
