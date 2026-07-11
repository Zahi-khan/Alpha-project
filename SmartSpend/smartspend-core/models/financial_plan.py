"""A route toward a goal, including planned contributions and constraints."""

from __future__ import annotations

from dataclasses import field
from decimal import Decimal
from typing import Any
from uuid import uuid4

from models._dataclasses import slotted_dataclass
from models.financial_constraint import FinancialConstraint
from models.milestone import Milestone


@slotted_dataclass(frozen=True)
class FinancialPlan:
    goal_id: str
    planned_monthly_contribution: Decimal
    constraints: tuple[FinancialConstraint, ...] = ()
    milestones: tuple[Milestone, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"plan_{uuid4().hex}")
