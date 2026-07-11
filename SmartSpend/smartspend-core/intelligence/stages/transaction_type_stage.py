"""Resolve the financial event type independently of spending category."""

from intelligence.evidence.evidence import Evidence
from intelligence.evidence.evidence_types import EvidenceType
from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage


class TransactionTypeStage(EnrichmentStage):
    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        amount = context.transaction.amount
        context.transaction_type = "income" if amount > 0 else "expense"
        context.add_evidence(
            Evidence(
                EvidenceType.TRANSACTION_TYPE,
                f"Amount sign indicates {context.transaction_type}.",
                source="amount_sign",
            )
        )
        return context
