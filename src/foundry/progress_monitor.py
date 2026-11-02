from __future__ import annotations

import hashlib
from collections import deque
from enum import Enum
from typing import Any


class ProgressVerdict(str, Enum):
    PROGRESSING = "progressing"
    EXACT_REPETITION = "exact_repetition"
    CYCLE_DETECTED = "cycle_detected"
    STAGNATION = "stagnation"
    BUDGET_EXCEEDED = "budget_exceeded"


class ExactStateRepeater:
    """Detects immediate repeated tool calls or state payloads."""

    def __init__(self, max_history: int = 10) -> None:
        self.history: deque[str] = deque(maxlen=max_history)

    def hash_payload(self, tool_name: str, args: dict[str, Any]) -> str:
        serialized = f"{tool_name}:{sorted(args.items())}"
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def record_and_check(self, tool_name: str, args: dict[str, Any]) -> bool:
        h = self.hash_payload(tool_name, args)
        if self.history and self.history[-1] == h:
            return True  # Exact consecutive repetition
        self.history.append(h)
        return False


class CycleDetector:
    """Detects alternating cycles in state trajectories (e.g. S1 -> S2 -> S1)."""

    def __init__(self, max_history: int = 20) -> None:
        self.history: list[str] = []
        self.max_history = max_history

    def record_and_check(self, state_signature: str) -> bool:
        self.history.append(state_signature)
        if len(self.history) > self.max_history:
            self.history.pop(0)

        # Check for cycles of period 2 to 4
        for period in (2, 3, 4):
            if len(self.history) >= period * 2:
                pattern1 = self.history[-period:]
                pattern2 = self.history[-2 * period : -period]
                if pattern1 == pattern2:
                    return True
        return False


class ProgressMonitor:
    """Unified watchdog monitoring agent trajectory health."""

    def __init__(
        self,
        max_steps: int = 20,
        max_cost_usd: float = 2.0,
    ) -> None:
        self.max_steps = max_steps
        self.max_cost_usd = max_cost_usd
        self.repeater = ExactStateRepeater()
        self.cycle_detector = CycleDetector()
        self.step_count = 0
        self.accumulated_cost = 0.0

    def step(
        self,
        tool_name: str,
        tool_args: dict[str, Any],
        state_repr: str,
        step_cost_usd: float = 0.0,
    ) -> ProgressVerdict:
        self.step_count += 1
        self.accumulated_cost += step_cost_usd

        if self.step_count > self.max_steps or self.accumulated_cost > self.max_cost_usd:
            return ProgressVerdict.BUDGET_EXCEEDED

        if self.repeater.record_and_check(tool_name, tool_args):
            return ProgressVerdict.EXACT_REPETITION

        if self.cycle_detector.record_and_check(state_repr):
            return ProgressVerdict.CYCLE_DETECTED

        return ProgressVerdict.PROGRESSING
