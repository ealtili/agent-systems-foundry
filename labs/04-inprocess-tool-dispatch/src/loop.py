"""The minimal tool-use loop. You implement it; tests/test_loop.py is the contract."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol

from src.registry import Registry


@dataclass(frozen=True)
class ModelTurn:
    content: list[dict[str, Any]]
    stop_reason: str


class Completer(Protocol):
    def __call__(self, messages: list[dict[str, Any]]) -> ModelTurn: ...


class LoopBudgetError(Exception):
    """The loop hit max_turns or its deadline."""


class TruncatedToolCallError(Exception):
    """The model ran out of tokens while writing a tool call; its input cannot be trusted."""


@dataclass(frozen=True)
class LoopResult:
    final_text: str
    messages: list[dict[str, Any]]
    turns: int
    tool_calls: int


def run_loop(
    complete: Completer,
    registry: Registry,
    task: str,
    *,
    max_turns: int,
    deadline_s: float,
    clock: Callable[[], float],
) -> LoopResult:
    """Drive model -> tools -> model until the model finishes.

    - messages start as [{"role": "user", "content": task}].
    - Before EVERY model call: if clock() - start > deadline_s, or max_turns calls have already
      been made, raise LoopBudgetError. `start` is clock() at entry. No check after tools run.
    - Append the model's content to messages UNCHANGED as an assistant message.
    - stop_reason "tool_use": dispatch every tool_use block, append ONE user message with all
      results (see build_result_message), continue. No tool_use block is a ValueError.
    - stop_reason "max_tokens" with a tool_use block present: raise TruncatedToolCallError and run
      nothing.
    - stop_reason "end_turn": return LoopResult with final_text = the text blocks joined by "".
    - Any other stop_reason: raise ValueError (handle it deliberately, do not guess).
    - LoopResult.turns counts model calls; tool_calls counts dispatched calls.
    """
    raise NotImplementedError
