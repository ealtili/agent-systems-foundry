from typing import Any

from src.dispatch import ToolCall
from src.scoring import selection_correct


def call(name: str, **args: object) -> ToolCall:
    return ToolCall("tu", name, args)


def test_no_tool_expected() -> None:
    expect: dict[str, Any] = {"tool": None, "args_subset": {}}
    assert selection_correct(expect, None) is True
    assert selection_correct(expect, call("get_order", order_id=1)) is False


def test_tool_expected_but_none_made() -> None:
    assert selection_correct({"tool": "get_order", "args_subset": {}}, None) is False


def test_name_and_args_must_match() -> None:
    expect = {"tool": "list_orders", "args_subset": {"customer": "Ada Lovelace", "limit": 3}}
    assert selection_correct(expect, call("list_orders", customer="ada lovelace ", limit="3"))
    assert not selection_correct(expect, call("get_order", customer="Ada Lovelace", limit=3))
    assert not selection_correct(expect, call("list_orders", customer="Ada Lovelace"))
    assert not selection_correct(expect, call("list_orders", customer="Grace Hopper", limit=3))


def test_extra_arguments_are_fine() -> None:
    expect = {"tool": "list_orders", "args_subset": {"status": "shipped"}}
    assert selection_correct(expect, call("list_orders", status="shipped", limit=2))
