"""Direct category-to-transaction lookup."""

from __future__ import annotations

from memory.events import TransactionProcessed
from memory.indexes._index import TransactionIndex


class CategoryIndex(TransactionIndex):
    def key_for(self, event: TransactionProcessed) -> str | None:
        category = event.enriched_transaction.category
        return category.id if category is not None else None
