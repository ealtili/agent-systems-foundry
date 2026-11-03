import json
from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict, Field
from src.registry import Registry, Tool
from src.schema import GetOrderArgs
from src.store import OrderStore
from src.tools import make_registry


def _noop(_: Any) -> str:
    return "ok"


def _has_title_keyword(schema: dict[str, Any]) -> bool:
    if "title" in schema:
        return True
    for key, value in schema.items():
        if key == "properties":
            if any(_has_title_keyword(p) for p in value.values()):
                return True
        elif (
            isinstance(value, dict)
            and _has_title_keyword(value)
            or isinstance(value, list)
            and any(isinstance(v, dict) and _has_title_keyword(v) for v in value)
        ):
            return True
    return False


def test_register_get_and_sorted_names() -> None:
    registry = Registry()
    registry.register(Tool("b_tool", "d", GetOrderArgs, _noop))
    registry.register(Tool("a_tool", "d", GetOrderArgs, _noop))
    assert registry.names() == ["a_tool", "b_tool"]
    assert registry.get("a_tool") is not None
    assert registry.get("missing") is None


def test_duplicate_and_bad_names_are_rejected() -> None:
    registry = Registry()
    registry.register(Tool("ok_name", "d", GetOrderArgs, _noop))
    with pytest.raises(ValueError):
        registry.register(Tool("ok_name", "d", GetOrderArgs, _noop))
    for bad in ["Bad", "1abc", "", "a-b", "x" * 65]:
        with pytest.raises(ValueError):
            registry.register(Tool(bad, "d", GetOrderArgs, _noop))


def test_schema_shape_for_get_order() -> None:
    schemas = make_registry(OrderStore.from_fixture()).schemas()
    assert [s["name"] for s in schemas] == ["get_order", "list_orders", "refund_order"]
    assert all(set(s) == {"name", "description", "input_schema"} for s in schemas)
    assert schemas[0]["input_schema"] == {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "integer",
                "minimum": 1,
                "description": "Numeric order id, for example 1003",
            }
        },
        "required": ["order_id"],
        "additionalProperties": False,
    }


def test_no_title_noise_and_closed_objects() -> None:
    for s in make_registry(OrderStore.from_fixture()).schemas():
        assert not _has_title_keyword(s["input_schema"])
        assert s["input_schema"]["additionalProperties"] is False


def test_a_property_named_title_is_kept() -> None:
    class Doc(BaseModel):
        model_config = ConfigDict(extra="forbid")
        title: str = Field(..., description="d")

    registry = Registry()
    registry.register(Tool("doc_tool", "d", Doc, _noop))
    schema = registry.schemas()[0]["input_schema"]
    assert "title" in schema["properties"]
    assert not _has_title_keyword(schema)


def test_schemas_are_byte_stable_and_order_independent() -> None:
    first = make_registry(OrderStore.from_fixture())
    again = Registry()
    for name in reversed(first.names()):
        tool = first.get(name)
        assert tool is not None
        again.register(tool)
    assert json.dumps(first.schemas()) == json.dumps(first.schemas())
    assert json.dumps(first.schemas()) == json.dumps(again.schemas())


def test_strict_flag() -> None:
    registry = make_registry(OrderStore.from_fixture())
    assert all("strict" not in s for s in registry.schemas())
    assert all(s["strict"] is True for s in registry.schemas(strict=True))
