"""In-memory order store. Given code: domain logic, not the point of the lab."""

import json
from pathlib import Path
from typing import Any

from src.schema import ToolError

ORDERS_FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "orders.json"


class OrderStore:
    def __init__(self, orders: list[dict[str, Any]]) -> None:
        self.orders: dict[int, dict[str, Any]] = {int(o["id"]): dict(o) for o in orders}

    @classmethod
    def from_fixture(cls, path: Path = ORDERS_FIXTURE) -> "OrderStore":
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def get(self, order_id: int) -> dict[str, Any]:
        order = self.orders.get(order_id)
        if order is None:
            raise ToolError(f"order {order_id} not found")
        return dict(order)

    def list(self, customer: str | None, status: str | None, limit: int) -> list[dict[str, Any]]:
        rows = [
            o
            for o in self.orders.values()
            if (customer is None or o["customer"].casefold() == customer.strip().casefold())
            and (status is None or o["status"] == status)
        ]
        rows.sort(key=lambda o: int(o["id"]), reverse=True)
        return [dict(o) for o in rows[:limit]]

    def refund(self, order_id: int, amount_cents: int, reason: str) -> dict[str, Any]:
        order = self.orders.get(order_id)
        if order is None:
            raise ToolError(f"order {order_id} not found")
        if order["status"] != "delivered":
            raise ToolError(
                f"order {order_id} is {order['status']}; only delivered orders can be refunded"
            )
        balance = int(order["total_cents"]) - int(order["refunded_cents"])
        if amount_cents > balance:
            raise ToolError(f"amount exceeds the refundable balance of {balance} cents")
        order["refunded_cents"] = int(order["refunded_cents"]) + amount_cents
        if order["refunded_cents"] == order["total_cents"]:
            order["status"] = "refunded"
        return {
            "order_id": order_id,
            "refunded_cents": order["refunded_cents"],
            "status": order["status"],
        }
