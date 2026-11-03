from datetime import date, timedelta
from pathlib import Path

import pytest
from concepts import INTERVALS_DAYS, Store, due, grade, load, register, save

TODAY = date(2026, 11, 3)


def make_lab(tmp_path: Path, name: str = "01-demo") -> Path:
    lab = tmp_path / name
    lab.mkdir()
    (lab / "concepts.json").write_text(
        '[{"id": "a-concept", "question": "What is the invariant being enforced here?"},'
        ' {"id": "b-concept", "question": "Why does this fail under network jitter?"}]',
        encoding="utf-8",
    )
    return lab


def test_register_is_idempotent(tmp_path: Path) -> None:
    store = Store()
    lab = make_lab(tmp_path)
    assert register(store, lab, TODAY) == 2
    assert register(store, lab, TODAY) == 0


def test_pass_advances_box_and_interval(tmp_path: Path) -> None:
    store = Store()
    register(store, make_lab(tmp_path), TODAY)
    card = grade(store, "01-demo:a-concept", True, TODAY)
    assert card.box == 1
    assert card.due == TODAY + timedelta(days=INTERVALS_DAYS[0])
    card = grade(store, "01-demo:a-concept", True, TODAY)
    assert card.due == TODAY + timedelta(days=INTERVALS_DAYS[1])


def test_fail_resets_and_box_is_capped(tmp_path: Path) -> None:
    store = Store()
    register(store, make_lab(tmp_path), TODAY)
    for _ in range(10):
        card = grade(store, "01-demo:a-concept", True, TODAY)
    assert card.box == len(INTERVALS_DAYS)
    card = grade(store, "01-demo:a-concept", False, TODAY)
    assert card.box == 0
    assert card.due == TODAY + timedelta(days=1)


def test_due_excludes_active_lab_and_future(tmp_path: Path) -> None:
    store = Store()
    register(store, make_lab(tmp_path, "01-demo"), TODAY)
    register(store, make_lab(tmp_path, "02-other"), TODAY)
    grade(store, "02-other:a-concept", True, TODAY)  # pushed to the future
    ids = [c.id for c in due(store, TODAY, 10, exclude_lab="01-demo")]
    assert ids == ["02-other:b-concept"]


def test_roundtrip_and_validation(tmp_path: Path) -> None:
    store = Store()
    register(store, make_lab(tmp_path), TODAY)
    path = tmp_path / "state" / "s.json"
    save(store, path)
    assert load(path).cards.keys() == store.cards.keys()
    path.write_text('{"cards": {"x": {"id": "x"}}}', encoding="utf-8")
    with pytest.raises(ValueError):
        load(path)
