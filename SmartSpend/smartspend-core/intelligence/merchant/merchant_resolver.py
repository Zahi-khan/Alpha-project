"""Stage that resolves a merchant without changing the source transaction."""

from __future__ import annotations

from typing import Protocol

from intelligence.pipeline import EnrichmentStage
from models.enrichment import EnrichmentContext
from models.merchant import Merchant
from preprocessing.normalizer import normalize_merchant


class MerchantMatcher(Protocol):
    def match(self, query: str) -> Merchant | None:
        """Return a merchant when this strategy can identify one."""


class MerchantResolver(EnrichmentStage):
    """Tries supplied matching strategies in order and records their evidence."""

    def __init__(self, *matchers: MerchantMatcher):
        self._matchers = matchers

    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        description = context.cleaned_description or context.transaction.description
        candidates = (description, normalize_merchant(description))

        for matcher in self._matchers:
            for candidate in candidates:
                merchant = matcher.match(candidate)
                if merchant is None:
                    continue
                context.resolved_merchant = merchant
                context.evidence["merchant_match"] = {
                    "query": candidate,
                    "strategy": type(matcher).__name__,
                    "merchant_id": merchant.id,
                }
                return context

        context.warnings.append("Merchant could not be resolved.")
        return context
