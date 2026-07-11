"""Final consistency checks for completed enrichment contexts."""

from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage


class ValidationStage(EnrichmentStage):
    """Reports contradictory resolved knowledge without altering source facts."""

    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        merchant = context.resolved_merchant
        if merchant is None:
            return context
        if context.resolved_category is not None and merchant.category != context.resolved_category:
            context.warnings.append("Resolved category conflicts with merchant knowledge.")
        if context.resolved_industry is not None and merchant.industry != context.resolved_industry:
            context.warnings.append("Resolved industry conflicts with merchant knowledge.")
        return context
