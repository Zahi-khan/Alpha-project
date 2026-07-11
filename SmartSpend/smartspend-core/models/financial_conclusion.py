"""Explainable interpretations derived from multiple financial insights."""

from __future__ import annotations

from dataclasses import field
from datetime import datetime
from typing import Any
from uuid import uuid4

from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class FinancialConclusion:
    title: str
    summary: str
    supporting_insight_ids: tuple[str, ...]
    confidence: float = 0.0
    severity: str = "informational"
    evidence: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.utcnow)
    id: str = field(default_factory=lambda: f"conclusion_{uuid4().hex}")
