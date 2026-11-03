import pytest
from src.schema import ToolError
from src.store import OrderStore


def test_get_and_not_found() -> None:
    store = OrderStore.from_fixture()
    assert store.get(1003)["status"] == "shipped"
    with pytest.raises(ToolError):
        store.get(9999)


def test_list_filters_sorts_and_limits() -> None:
    store = OrderStore.from_fixture()
    assert [o["id"] for o in store.list(None, "shipped", 2)] == [1011, 1009]
    assert [o["id"] for o in store.list("ada lovelace", None, 10)] == [1012, 1006, 1002, 1001]


def test_refund_rules() -> None:
    store = OrderStore.from_fixture()
    assert store.refund(1002, 500, "damaged")["refunded_cents"] == 500
    with pytest.raises(ToolError):
        store.refund(1001, 100, "pending order")
    with pytest.raises(ToolError):
        store.refund(1002, 99_999, "too much")
    assert store.refund(1002, 11_500, "rest")["status"] == "refunded"
