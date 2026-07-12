"""Extract UPI app, counterparty, and reference context without inventing a merchant."""

from __future__ import annotations

import re

from intelligence.evidence.evidence import Evidence
from intelligence.evidence.evidence_types import EvidenceType
from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage


class PaymentContextStage(EnrichmentStage):
    _UPI_ID = re.compile(r"(?<![\w.-])([\w.-]+@[\w.-]+)", re.IGNORECASE)
    _REFERENCE = re.compile(r"(?<!\d)(\d{10,16})(?!\d)")
    _AGGREGATORS = {
        "AMAZON PAY": "Amazon Pay", "AMAZONPAY": "Amazon Pay",
        "GOOGLE PAY": "Google Pay", "GOOGLE IND": "Google Pay", "GPAY": "Google Pay",
        "PAYTM": "Paytm", "PHONEPE": "PhonePe", "RAZORPAY": "Razorpay", "CASHFREE": "Cashfree",
    }

    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        raw = str(context.transaction.metadata.get("description") or context.transaction.description).strip()
        upper = raw.upper()
        if "UPI" not in upper:
            return context

        vendor = str(context.transaction.metadata.get("vendor") or context.transaction.description).strip()
        party_hint = _upi_party(raw)
        aggregator = next(
            (name for marker, name in self._AGGREGATORS.items() if marker in vendor.upper() or marker in party_hint.upper()),
            None,
        )
        upi_match = self._UPI_ID.search(raw)
        reference_match = self._REFERENCE.search(raw)
        context.metadata.update({
            "payment_rail": "UPI",
            "payment_initiator": aggregator,
            "counterparty": vendor or None,
            "beneficiary_vpa": upi_match.group(1) if upi_match else None,
            "payment_reference": reference_match.group(1) if reference_match else None,
        })
        if aggregator and _same_party(vendor, aggregator):
            context.metadata["merchant_visibility"] = "not_visible"
            context.warnings.append(f"Paid through {aggregator}; the final merchant was not visible in this statement.")
            evidence = f"Detected {aggregator} as a payment app or gateway; no final merchant was visible."
        else:
            context.metadata["merchant_visibility"] = "visible"
            evidence = "UPI payment context was extracted from the statement narration."
        context.add_evidence(Evidence(EvidenceType.PAYMENT_DETECTION, evidence, source="upi_context", score=0.85))
        return context


def _same_party(left: str, right: str) -> bool:
    normalize = lambda value: " ".join("".join(char if char.isalnum() else " " for char in value.casefold()).split())
    normalized_left, normalized_right = normalize(left), normalize(right)
    if normalized_left in normalized_right or normalized_right in normalized_left:
        return True
    return bool(normalized_left and normalized_right and normalized_left.split()[0] == normalized_right.split()[0])


def _upi_party(raw: str) -> str:
    match = re.search(r"\bUPI[/:_-]+([^/\n]+)", raw, re.IGNORECASE)
    return match.group(1).strip() if match else ""
