"""Facts observed for industries over time."""

from __future__ import annotations

from memory.events import TransactionProcessed
from memory.history._entity_history import EntityHistory


class IndustryHistory(EntityHistory):
    def key_for(self, event: TransactionProcessed) -> str | None:
        industry = event.enriched_transaction.industry
        return industry.id if industry is not None else None
