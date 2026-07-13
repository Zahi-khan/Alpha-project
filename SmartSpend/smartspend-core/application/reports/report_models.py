"""Internal report data with only aggregated, safe-to-display information."""

from __future__ import annotations

from dataclasses import field
from datetime import datetime
from typing import Any

from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class FinancialReport:
    generated_at: datetime
    summary: dict[str, Any]
    metrics: tuple[dict, ...] = ()
    charts: tuple[dict, ...] = ()
    insights: tuple[dict, ...] = ()
    conclusions: tuple[dict, ...] = ()
    warnings: tuple[str, ...] = ()
