from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    step_id: int = Field(..., description="Sequential step index")
    action: str = Field(..., description="Action to execute")
    expected_outcome: str = Field(..., description="Observable result of this action")


class StructuredPlan(BaseModel):
    objective: str = Field(..., description="High-level goal")
    steps: list[PlanStep] = Field(..., min_length=1, description="List of planned steps")
    estimated_duration_minutes: int = Field(default=10)
