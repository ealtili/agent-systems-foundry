from pydantic import BaseModel, ConfigDict, Field


class Verdict(BaseModel):
    """System B output contract. Validated at the trust boundary (model output is untrusted)."""

    model_config = ConfigDict(extra="forbid")

    answer: str = Field(..., min_length=1, description="Final answer only, no explanation")
    evidence: list[str] = Field(
        default_factory=list, description="Short statements the answer relies on"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Stated probability that the answer is correct"
    )
