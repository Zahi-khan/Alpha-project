"""Filter transactions by industry ID."""

from memory.enriched_transaction import EnrichedTransaction


class IndustryFilter:
    def __init__(self, industry_id: str): self.industry_id = industry_id
    def matches(self, item: EnrichedTransaction) -> bool:
        return item.industry is not None and item.industry.id == self.industry_id
