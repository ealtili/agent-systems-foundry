from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ToolResult(BaseModel):
    """Normalized result returned from an ACI tool execution."""

    success: bool
    output: str
    error: str | None = None
    execution_time_ms: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class ToolDefinition(BaseModel):
    """Specification of a tool exposed to an agent."""

    name: str
    description: str
    parameters_schema: dict[str, Any]
    timeout_seconds: float = 30.0
    requires_approval: bool = False


class ResultMessage[T](BaseModel):
    """Standardized envelope for agent completion."""

    status: str
    data: T | None = None
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    step_count: int = 0
    completed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AgentState(BaseModel):
    """Base class for all boundary-crossing agent state models."""

    session_id: str
    step: int = 0
    max_steps: int = 25
    is_terminal: bool = False
    context_tokens: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)
