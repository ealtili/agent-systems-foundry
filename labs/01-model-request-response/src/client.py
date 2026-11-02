from __future__ import annotations

import json
from typing import Any
from pydantic import ValidationError
from schema import StructuredPlan


class PlanExtractor:
    """Extracts and validates structured plan objects from model output."""

    @staticmethod
    def parse_raw_json(raw_text: str) -> tuple[StructuredPlan | None, str | None]:
        clean_text = raw_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()

        try:
            data = json.loads(clean_text)
            plan = StructuredPlan.model_validate(data)
            return plan, None
        except (json.JSONDecodeError, ValidationError) as err:
            return None, str(err)
