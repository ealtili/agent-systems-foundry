"""Tool-call dispatch. You implement it; tests/test_dispatch.py is the contract."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from src.registry import Registry


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    input: Mapping[str, Any]


@dataclass(frozen=True)
class ToolResult:
    tool_use_id: str
    content: str
    is_error: bool = False


def extract_tool_calls(content: Sequence[Mapping[str, Any]]) -> list[ToolCall]:
    """The tool_use blocks of an assistant message, in order. Other block types are ignored."""
    raise NotImplementedError


def dispatch(registry: Registry, call: ToolCall) -> ToolResult:
    """Run one tool call and return what the model should see.

    - Unknown tool: is_error, content "unknown_tool: <name>. Available: a, b, c" (sorted names).
    - Arguments that fail validation against the args model: is_error, content starting with
      "invalid_arguments:" followed by one line "- <location>: <message>" per problem, sorted
      by location. Unknown extra fields are a problem.
    - Handler raises ToolError: is_error, content "tool_error: <message>".
    - Success: the handler's string, is_error False.
    Any other exception is a harness bug and must propagate.
    """
    raise NotImplementedError


def build_result_message(results: Sequence[ToolResult]) -> dict[str, Any]:
    """The single user message that answers one assistant turn.

    {"role": "user", "content": [{"type": "tool_result", "tool_use_id": ..., "content": ...}, ...]}
    in the order given; "is_error": True is present only on failed results. Raises ValueError
    for no results or duplicate tool_use_ids.
    """
    raise NotImplementedError
