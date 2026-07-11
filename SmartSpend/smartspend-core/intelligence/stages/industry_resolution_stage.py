"""Resolve industry exclusively from already-resolved merchant knowledge."""

from intelligence.evidence.evidence import Evidence
from intelligence.evidence.evidence_types import EvidenceType
from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage


class IndustryResolutionStage(EnrichmentStage):
    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        merchant = context.resolved_merchant
        if merchant is None or merchant.industry is None:
            return context
        context.resolved_industry = merchant.industry
        context.add_evidence(
            Evidence(
                EvidenceType.INDUSTRY_LINK,
                f'Merchant "{merchant.canonical_name}" links to "{merchant.industry.name}".',
                source="merchant_knowledge",
            )
        )
        return context
