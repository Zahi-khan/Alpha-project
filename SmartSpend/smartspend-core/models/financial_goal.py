"""A user-defined financial destination, independent of recommendations."""

from __future__ import annotations

from dataclasses import field
from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class FinancialGoal:
    name: str
    target_amount: Decimal
    target_date: datetime
    currency: str = "INR"
    priority: str = "normal"
    category_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"goal_{uuid4().hex}")
