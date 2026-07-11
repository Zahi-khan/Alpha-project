"""A time-stamped factual assessment of progress toward one goal."""

from __future__ import annotations

from dataclasses import field
from datetime import datetime
from decimal import Decimal
from typing import Any

from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class GoalProgress:
    goal_id: str
    as_of: datetime
    current_amount: Decimal
    remaining_amount: Decimal
    progress_ratio: Decimal
    required_monthly_contribution: Decimal
    planned_monthly_contribution: Decimal
    monthly_gap: Decimal
    on_track: bool
    projected_completion: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
