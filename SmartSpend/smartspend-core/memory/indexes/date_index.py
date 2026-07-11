"""Direct calendar-date-to-transaction lookup."""

from __future__ import annotations

from memory.events import TransactionProcessed
from memory.indexes._index import TransactionIndex


class DateIndex(TransactionIndex):
    def key_for(self, event: TransactionProcessed) -> str | None:
        date = event.enriched_transaction.transaction.date
        return date.date().isoformat() if date is not None else None
