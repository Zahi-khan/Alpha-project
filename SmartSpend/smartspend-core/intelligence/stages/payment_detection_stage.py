"""Detect payment family and method without resolving any merchant."""

from intelligence.evidence.evidence import Evidence
from intelligence.evidence.evidence_types import EvidenceType
from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage
from intelligence.results.resolved_payment import ResolvedPayment


class PaymentDetectionStage(EnrichmentStage):
    _MARKERS = (
        ("UPI", "Digital", "UPI"),
        ("CREDIT CARD", "Card", "Credit Card"),
        ("DEBIT CARD", "Card", "Debit Card"),
        ("NEFT", "Bank Transfer", "NEFT"),
        ("IMPS", "Bank Transfer", "IMPS"),
        ("RTGS", "Bank Transfer", "RTGS"),
        ("AUTO-DEBIT", "Direct Debit", "Auto-Debit"),
        ("AUTO DEBIT", "Direct Debit", "Auto-Debit"),
        ("CASH", "Cash", "Cash"),
    )

    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        supplied_mode = str(context.transaction.metadata.get("mode", "")).strip()
        raw = f"{context.transaction.description} {supplied_mode}".upper()
        for marker, family, method in self._MARKERS:
            if marker in raw:
                context.payment = ResolvedPayment(family=family, method=method)
                context.add_evidence(
                    Evidence(EvidenceType.PAYMENT_DETECTION, f"Detected {method}.", source="statement_mode" if supplied_mode else marker, score=0.90 if supplied_mode else None)
                )
                return context
        return context
