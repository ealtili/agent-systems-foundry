import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def _rows(name: str) -> list[dict[str, object]]:
    lines = (FIXTURES / name).read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def test_handbook_is_long_enough_to_cache() -> None:
    text = (FIXTURES / "handbook.md").read_text(encoding="utf-8")
    assert text.count("\nRule ") == 60
    assert len(text) > 15_000  # roughly 4k tokens; confirm with count_tokens before a live run


def test_turns_are_numbered_and_answerable() -> None:
    turns = _rows("turns.jsonl")
    assert [t["turn"] for t in turns] == list(range(1, 11))
    assert all(str(t["answer"]) for t in turns)


def test_recorded_usage_is_synthetic_and_complete() -> None:
    rows = _rows("recorded_usage.jsonl")
    assert len(rows) == 30
    assert all(r["synthetic"] is True for r in rows)
    assert {r["scenario"] for r in rows} == {"uncached", "cached_ok", "cached_invalidated"}
