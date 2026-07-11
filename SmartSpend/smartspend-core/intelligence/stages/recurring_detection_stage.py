"""Reserved stage for history-aware recurring-payment detection."""

from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage


class RecurringDetectionStage(EnrichmentStage):
    """Leaves the context unchanged until transaction history is supplied."""

    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        return context
