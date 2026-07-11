"""Future action contract derived from conclusions, never raw transactions."""

from __future__ import annotations

from dataclasses import field
from datetime import datetime
from typing import Any
from uuid import uuid4

from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class Recommendation:
    title: str
    summary: str
    supporting_conclusion_ids: tuple[str, ...]
    priority: str = "normal"
    confidence: float = 0.0
    expected_impact: dict[str, Any] = field(default_factory=dict)
    goal_alignment: dict[str, Any] = field(default_factory=dict)
    evidence: tuple[str, ...] = ()
    reasoning_path: tuple[str, ...] = ()
    suggested_actions: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.utcnow)
    id: str = field(default_factory=lambda: f"recommendation_{uuid4().hex}")
