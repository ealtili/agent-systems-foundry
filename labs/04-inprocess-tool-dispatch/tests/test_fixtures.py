import json
from pathlib import Path
from typing import Any

import pytest
from src.schema import ToolError
from src.store import OrderStore

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def _rows(name: str) -> list[dict[str, Any]]:
    lines = (FIXTURES / name).read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def test_task_answers_are_proven_by_the_store() -> None:
    tasks = {t["id"]: t for t in _rows("tasks.jsonl")}
    store = OrderStore.from_fixture()
    assert store.get(1003)["status"] == tasks["t1"]["answer"]
    assert str(len(store.list("Ada Lovelace", None, 50))) == tasks["t2"]["answer"]
    assert str(store.get(1007)["total_cents"]) == tasks["t3"]["answer"]
    delivered = sorted(o["id"] for o in store.list("Grace Hopper", "delivered", 50))
    assert ",".join(map(str, delivered)) == tasks["t4"]["answer"]
    pending = [o["total_cents"] for o in store.list(None, "pending", 50)]
    assert str(max(pending)) == tasks["t7"]["answer"]
    shipped = [o["id"] for o in store.list(None, "shipped", 2)]
    assert ",".join(map(str, shipped)) == tasks["t8"]["answer"]


def test_mutating_tasks_have_the_expected_final_state() -> None:
    tasks = {t["id"]: t for t in _rows("tasks.jsonl")}
    store = OrderStore.from_fixture()
    store.refund(1002, 500, "damaged")
    for oid, expected in tasks["t5"]["final_state"].items():
        for key, value in expected.items():
            assert store.orders[int(oid)][key] == value
    with pytest.raises(ToolError):
        OrderStore.from_fixture().refund(1001, 4500, "changed mind")


def test_selection_cases_are_well_formed() -> None:
    cases = _rows("selection_cases.jsonl")
    assert len(cases) == 12
    assert len({c["id"] for c in cases}) == 12
    tools = {c["expect"]["tool"] for c in cases}
    assert tools <= {None, "get_order", "list_orders", "refund_order"}
    assert sum(1 for c in cases if c["expect"]["tool"] is None) == 2
