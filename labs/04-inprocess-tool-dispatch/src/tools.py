"""Wiring of the order store into a Registry. Given code; the Registry itself is yours."""

import json
from collections.abc import Mapping
from typing import Any

from src.registry import Registry, Tool
from src.schema import GetOrderArgs, ListOrdersArgs, RefundOrderArgs
from src.store import OrderStore

# Deliberately thin first-draft descriptions. Writing better ones is part of the lab (P3).
DEFAULT_DESCRIPTIONS: dict[str, str] = {
    "get_order": "Get an order.",
    "list_orders": "List orders.",
    "refund_order": "Refund an order.",
}


def _dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def make_registry(store: OrderStore, descriptions: Mapping[str, str] | None = None) -> Registry:
    text = {**DEFAULT_DESCRIPTIONS, **(descriptions or {})}

    def get_order(args: GetOrderArgs) -> str:
        return _dump(store.get(args.order_id))

    def list_orders(args: ListOrdersArgs) -> str:
        return _dump(store.list(args.customer, args.status, args.limit))

    def refund_order(args: RefundOrderArgs) -> str:
        return _dump(store.refund(args.order_id, args.amount_cents, args.reason))

    registry = Registry()
    registry.register(Tool("get_order", text["get_order"], GetOrderArgs, get_order))
    registry.register(Tool("list_orders", text["list_orders"], ListOrdersArgs, list_orders))
    registry.register(Tool("refund_order", text["refund_order"], RefundOrderArgs, refund_order))
    return registry
