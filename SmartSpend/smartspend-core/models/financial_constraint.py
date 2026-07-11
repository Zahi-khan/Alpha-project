"""A user-set decision boundary, separate from goals and budgets."""

from __future__ import annotations

from dataclasses import field
from decimal import Decimal
from typing import Any
from uuid import uuid4

from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class FinancialConstraint:
    name: str
    constraint_type: str
    amount: Decimal | None = None
    category_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"constraint_{uuid4().hex}")
