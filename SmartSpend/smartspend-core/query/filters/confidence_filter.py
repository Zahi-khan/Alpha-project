"""Filter transactions by minimum enrichment confidence."""

from memory.enriched_transaction import EnrichedTransaction


class ConfidenceFilter:
    def __init__(self, minimum: float): self.minimum = minimum
    def matches(self, item: EnrichedTransaction) -> bool: return item.confidence >= self.minimum
