import pytest
from src.client import PlanExtractor
from src.schema import StructuredPlan


def test_valid_json_parsing() -> None:
    raw_payload = """```json
    {
        "objective": "Build secure agent harness",
        "steps": [
            {
                "step_id": 1,
                "action": "Define boundary models",
                "expected_outcome": "Pydantic models created"
            }
        ],
        "estimated_duration_minutes": 15
    }
    ```"""
    plan, error = PlanExtractor.parse_raw_json(raw_payload)
    assert error is None
    assert isinstance(plan, StructuredPlan)
    assert plan.objective == "Build secure agent harness"
    assert len(plan.steps) == 1
    assert plan.steps[0].step_id == 1


def test_invalid_schema_caught() -> None:
    # Missing required 'steps' field
    invalid_payload = '{"objective": "Incomplete plan"}'
    plan, error = PlanExtractor.parse_raw_json(invalid_payload)
    assert plan is None
    assert error is not None
    assert "steps" in error
