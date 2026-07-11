"""Aggregate confidence only after discovery stages have contributed evidence."""

from intelligence.evidence.score import score_evidence
from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage


class ConfidenceStage(EnrichmentStage):
    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        context.confidence = score_evidence(context)
        return context
