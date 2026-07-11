"""Resolve category from merchant knowledge, never from merchant aliases."""

from intelligence.evidence.evidence import Evidence
from intelligence.evidence.evidence_types import EvidenceType
from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage


class CategoryResolutionStage(EnrichmentStage):
    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        merchant = context.resolved_merchant
        if merchant is None or merchant.category is None:
            return context
        context.resolved_category = merchant.category
        context.add_evidence(
            Evidence(
                EvidenceType.CATEGORY_LINK,
                f'Merchant "{merchant.canonical_name}" links to "{merchant.category.name}".',
                source="merchant_knowledge",
            )
        )
        return context
