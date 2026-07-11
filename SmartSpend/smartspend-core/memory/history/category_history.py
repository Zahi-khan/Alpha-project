"""Facts observed for categories over time."""

from __future__ import annotations

from memory.events import TransactionProcessed
from memory.history._entity_history import EntityHistory


class CategoryHistory(EntityHistory):
    def key_for(self, event: TransactionProcessed) -> str | None:
        category = event.enriched_transaction.category
        return category.id if category is not None else None
