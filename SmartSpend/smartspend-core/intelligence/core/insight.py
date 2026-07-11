"""Traceable, presentation-independent financial conclusions."""

from __future__ import annotations

from dataclasses import field
from datetime import datetime
from typing import Any
from uuid import uuid4

from intelligence.core.insight_type import InsightType
from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class FinancialInsight:
    insight_type: InsightType
    title: str
    summary: str
    severity: str = "informational"
    confidence: float = 0.0
    supporting_query: Any | None = None
    supporting_metrics: dict[str, Any] = field(default_factory=dict)
    supporting_evidence: tuple[str, ...] = ()
    generated_at: datetime = field(default_factory=datetime.utcnow)
    tags: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"insight_{uuid4().hex}")

    @property
    def affected_metrics(self) -> dict[str, Any]:
        """Compatibility name for existing consumers of supporting metrics."""
        return self.supporting_metrics
