"""Resolve the financial event type independently of spending category."""

from intelligence.evidence.evidence import Evidence
from intelligence.evidence.evidence_types import EvidenceType
from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage


class TransactionTypeStage(EnrichmentStage):
    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        supplied_type = str(context.transaction.metadata.get("type", "")).strip().casefold()
        if supplied_type in {"credit", "cr", "income"}:
            context.transaction_type = "income"
            source = "statement_type"
        elif supplied_type in {"debit", "dr", "expense"}:
            context.transaction_type = "expense"
            source = "statement_type"
        else:
            amount = context.transaction.amount
            context.transaction_type = "income" if amount > 0 else "expense"
            source = "amount_sign"
        context.add_evidence(
            Evidence(
                EvidenceType.TRANSACTION_TYPE,
                f"Amount sign indicates {context.transaction_type}.",
                source=source,
            )
        )
        return context
