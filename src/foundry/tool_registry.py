from __future__ import annotations

import asyncio
import inspect
import time
from typing import Any, Callable
from foundry.models import ToolDefinition, ToolResult


class ToolRegistry:
    """Registry managing tool schema generation and bounded execution."""

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}
        self._definitions: dict[str, ToolDefinition] = {}

    def register(
        self,
        name: str,
        description: str,
        timeout_seconds: float = 30.0,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self._tools[name] = func
            self._definitions[name] = ToolDefinition(
                name=name,
                description=description,
                parameters_schema=self._introspect_schema(func),
                timeout_seconds=timeout_seconds,
            )
            return func
        return decorator

    def _introspect_schema(self, func: Callable[..., Any]) -> dict[str, Any]:
        sig = inspect.signature(func)
        properties: dict[str, Any] = {}
        required: list[str] = []
        for param_name, param in sig.parameters.items():
            if param_name in ("self", "cls"):
                continue
            properties[param_name] = {"type": "string"}
            if param.default is inspect.Parameter.empty:
                required.append(param_name)
        return {
            "type": "object",
            "properties": properties,
            "required": required,
        }

    def get_definitions(self) -> list[ToolDefinition]:
        return list(self._definitions.values())

    async def execute(self, name: str, **kwargs: Any) -> ToolResult:
        if name not in self._tools:
            return ToolResult(
                success=False,
                output="",
                error=f"Tool '{name}' is not registered in this registry.",
            )
        func = self._tools[name]
        defn = self._definitions[name]
        start_time = time.perf_counter()

        try:
            async with asyncio.timeout(defn.timeout_seconds):
                if inspect.iscoroutinefunction(func):
                    res = await func(**kwargs)
                else:
                    res = func(**kwargs)
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return ToolResult(
                success=True,
                output=str(res),
                execution_time_ms=duration_ms,
            )
        except TimeoutError:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return ToolResult(
                success=False,
                output="",
                error=f"Execution exceeded deadline of {defn.timeout_seconds}s",
                execution_time_ms=duration_ms,
            )
        except Exception as ex:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return ToolResult(
                success=False,
                output="",
                error=f"Unhandled tool exception: {ex}",
                execution_time_ms=duration_ms,
            )
