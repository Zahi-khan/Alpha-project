"""Resolve a merchant using supplied matching strategies only."""

from __future__ import annotations

from typing import Protocol

from intelligence.evidence.evidence import Evidence
from intelligence.evidence.evidence_types import EvidenceType
from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage
from models.merchant import Merchant
from preprocessing.normalizer import normalize_merchant


class MerchantMatcher(Protocol):
    def match(self, query: str) -> Merchant | None:
        """Return a merchant when this strategy recognizes the query."""


class MerchantResolutionStage(EnrichmentStage):
    def __init__(self, *matchers: MerchantMatcher):
        self._matchers = matchers

    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        description = context.normalized_description or context.transaction.description
        candidates = (description, normalize_merchant(description))
        for matcher in self._matchers:
            for candidate in candidates:
                merchant = matcher.match(candidate)
                if merchant is None:
                    continue
                context.resolved_merchant = merchant
                context.add_evidence(
                    Evidence(
                        EvidenceType.MERCHANT_MATCH,
                        f'"{candidate}" resolved to "{merchant.canonical_name}".',
                        source=type(matcher).__name__,
                        metadata={"merchant_id": merchant.id},
                    )
                )
                return context
        context.warnings.append("Merchant could not be resolved.")
        return context
