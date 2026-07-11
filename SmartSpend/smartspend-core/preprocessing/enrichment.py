"""Compatibility stages for preprocessing before full knowledge resolution."""

from intelligence.pipeline import EnrichmentPipeline, EnrichmentStage
from intelligence.stages.normalization_stage import NormalizationStage
from models.enrichment import EnrichmentContext
from preprocessing.normalizer import normalize_merchant


class DescriptionNormalizationStage(NormalizationStage):
    """Backward-compatible name for the canonical normalization stage."""


class MerchantCandidateStage:
    """Stores a candidate only; it never claims to resolve a Merchant object."""

    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        description = context.normalized_description or context.transaction.description
        context.metadata["merchant_candidate"] = normalize_merchant(description)
        return context


__all__ = [
    "DescriptionNormalizationStage",
    "EnrichmentPipeline",
    "EnrichmentStage",
    "MerchantCandidateStage",
]
