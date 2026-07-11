"""The mutable working context shared by isolated intelligence stages."""

from __future__ import annotations

from dataclasses import field, replace
from typing import Any

from intelligence.evidence.evidence import Evidence
from intelligence.results.resolved_payment import ResolvedPayment
from models._dataclasses import slotted_dataclass
from models.category import Category
from models.industry import Industry
from models.merchant import Merchant
from models.transaction import Transaction


@slotted_dataclass
class EnrichmentContext:
    """Accumulates enrichment without changing the source transaction."""

    transaction: Transaction
    normalized_description: str | None = None
    resolved_merchant: Merchant | None = None
    resolved_category: Category | None = None
    resolved_industry: Industry | None = None
    payment: ResolvedPayment | None = None
    transaction_type: str | None = None
    evidence: list[Evidence] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    confidence: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_evidence(self, evidence: Evidence) -> None:
        self.evidence.append(evidence)

    def to_transaction(self) -> Transaction:
        """Materialize one enriched copy after every stage has completed."""
        metadata = {**self.transaction.metadata, **self.metadata}
        if self.evidence:
            metadata["enrichment_evidence"] = [item.to_dict() for item in self.evidence]
        if self.warnings:
            metadata["enrichment_warnings"] = list(self.warnings)

        return replace(
            self.transaction,
            cleaned_description=(
                self.normalized_description
                if self.normalized_description is not None
                else self.transaction.cleaned_description
            ),
            merchant=self.resolved_merchant or self.transaction.merchant,
            payment_method=(
                self.payment.method
                if self.payment is not None
                else self.transaction.payment_method
            ),
            transaction_type=self.transaction_type or self.transaction.transaction_type,
            confidence=(
                self.confidence
                if self.confidence is not None
                else self.transaction.confidence
            ),
            metadata=metadata,
        )

    def to_enriched_transaction(self):
        """Create the immutable handoff record for the financial memory layer."""
        from memory.enriched_transaction import EnrichedTransaction

        return EnrichedTransaction.from_context(self)
