"""Immutable description of a financial retrieval request."""

from __future__ import annotations

from dataclasses import field
from typing import Any
from uuid import uuid4

from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class FinancialQuery:
    filters: tuple[Any, ...] = ()
    group_by: Any | None = None
    metrics: tuple[Any, ...] = ()
    sort_by: str | None = None
    descending: bool = False
    limit: int | None = None
    output_format: str = "rows"
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"query_{uuid4().hex}")
