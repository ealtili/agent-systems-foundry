"""Tool-selection scoring. You implement it; tests/test_scoring.py is the contract."""

from collections.abc import Mapping
from typing import Any

from src.dispatch import ToolCall


def selection_correct(expect: Mapping[str, Any], call: ToolCall | None) -> bool:
    """Was the FIRST tool call what the case expected?

    `expect` is {"tool": name or None, "args_subset": {...}}. If expect["tool"] is None the
    model is correct only by making no tool call (call is None). Otherwise the call must exist,
    have that name, and for every key in args_subset the call's value must match after
    str(...).strip().casefold() on both sides. Extra arguments in the call are fine.
    """
    raise NotImplementedError
