import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def _rows(name: str) -> list[dict[str, object]]:
    lines = (FIXTURES / name).read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def test_questions_are_well_formed() -> None:
    rows = _rows("questions.jsonl")
    ids = [r["id"] for r in rows]
    assert len(rows) == 12
    assert len(set(ids)) == 12
    assert sum(1 for r in rows if r["kind"] == "unanswerable") == 1
    assert all(str(r["answer"]) == str(r["answer"]).strip().lower() for r in rows)


def test_recorded_runs_reference_known_questions_and_are_marked_synthetic() -> None:
    known = {r["id"] for r in _rows("questions.jsonl")}
    runs = _rows("recorded_runs.jsonl")
    assert runs
    assert all(r["synthetic"] is True for r in runs)
    assert all(r["question_id"] in known for r in runs)
    assert {r["system"] for r in runs} <= {"A", "B"}
    assert {r["effort"] for r in runs} <= {"low", "high"}
