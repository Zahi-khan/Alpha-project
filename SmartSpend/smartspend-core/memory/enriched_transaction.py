"""Immutable output of the intelligence pipeline and input to financial memory."""

from __future__ import annotations

from dataclasses import field
from typing import Any

from intelligence.evidence.evidence import Evidence
from intelligence.pipeline.context import EnrichmentContext
from intelligence.results.resolved_payment import ResolvedPayment
from models._dataclasses import slotted_dataclass
from models.category import Category
from models.industry import Industry
from models.merchant import Merchant
from models.transaction import Transaction


@slotted_dataclass(frozen=True)
class EnrichedTransaction:
    """A completed, explainable enrichment record that memory never mutates."""

    transaction: Transaction
    merchant: Merchant | None = None
    category: Category | None = None
    industry: Industry | None = None
    payment: ResolvedPayment | None = None
    transaction_type: str | None = None
    confidence: float = 0.0
    evidence: tuple[Evidence, ...] = ()
    processing_metadata: dict[str, Any] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()

    @classmethod
    def from_context(cls, context: EnrichmentContext) -> EnrichedTransaction:
        """Freeze the completed context without modifying its raw transaction."""
        return cls(
            transaction=context.to_transaction(),
            merchant=context.resolved_merchant,
            category=context.resolved_category,
            industry=context.resolved_industry,
            payment=context.payment,
            transaction_type=context.transaction_type,
            confidence=context.confidence or 0.0,
            evidence=tuple(context.evidence),
            processing_metadata=dict(context.metadata),
            warnings=tuple(context.warnings),
        )
