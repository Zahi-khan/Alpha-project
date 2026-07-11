"""A measurable checkpoint on the route to a financial goal."""

from __future__ import annotations

from dataclasses import field
from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class Milestone:
    name: str
    target_amount: Decimal
    due_date: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"milestone_{uuid4().hex}")
