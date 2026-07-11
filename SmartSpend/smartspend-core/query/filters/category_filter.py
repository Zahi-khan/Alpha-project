"""Filter transactions by category ID."""

from memory.enriched_transaction import EnrichedTransaction


class CategoryFilter:
    def __init__(self, category_id: str): self.category_id = category_id
    def matches(self, item: EnrichedTransaction) -> bool:
        return item.category is not None and item.category.id == self.category_id
