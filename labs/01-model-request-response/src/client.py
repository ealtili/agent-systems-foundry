from __future__ import annotations

from .schema import StructuredPlan


class PlanExtractor:
    """TODO(you): extract and validate a StructuredPlan from raw model output.

    Contract to design yourself: how fences, truncation and schema errors are
    reported. The signature below is only a placeholder.
    """

    @staticmethod
    def parse_raw_json(raw_text: str) -> tuple[StructuredPlan | None, str | None]:
        raise NotImplementedError("Lab 01: you write this.")
