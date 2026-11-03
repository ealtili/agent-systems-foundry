from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ToolError(Exception):
    """An expected, model-visible failure (not found, not allowed, out of range).

    Anything that is NOT a ToolError (or a validation error on the model's arguments) is a bug
    in the harness and must not be shown to the model.
    """


class _Args(BaseModel):
    model_config = ConfigDict(extra="forbid")


class GetOrderArgs(_Args):
    order_id: int = Field(..., ge=1, description="Numeric order id, for example 1003")


class ListOrdersArgs(_Args):
    customer: str | None = Field(default=None, description="Full customer name, e.g. Ada Lovelace")
    status: Literal["pending", "shipped", "delivered", "refunded"] | None = Field(
        default=None, description="Only orders in this status"
    )
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of orders to return")


class RefundOrderArgs(_Args):
    order_id: int = Field(..., ge=1, description="Numeric order id")
    amount_cents: int = Field(..., ge=1, description="Amount to refund, in cents")
    reason: str = Field(..., min_length=3, description="Short reason for the refund")
