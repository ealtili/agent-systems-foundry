import json
from pathlib import Path

from src.faults import SCENARIOS

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_recorded_runs_are_synthetic_and_cover_every_scenario() -> None:
    lines = (FIXTURES / "recorded_runs.jsonl").read_text(encoding="utf-8").splitlines()
    rows = [json.loads(line) for line in lines if line.strip()]
    assert all(r["synthetic"] is True for r in rows)
    assert {r["arm"] for r in rows} == {"A", "B"}
    assert {r["scenario"] for r in rows} == set(SCENARIOS) - {"dead"} | {"dead_burst"}
