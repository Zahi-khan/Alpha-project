"""An immutable explanation for a single enrichment decision."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from intelligence.evidence.evidence_types import EvidenceType
from models._dataclasses import slotted_dataclass


@slotted_dataclass
class Evidence:
    evidence_type: EvidenceType
    detail: str
    source: str | None = None
    score: float | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["evidence_type"] = self.evidence_type.value
        return result
