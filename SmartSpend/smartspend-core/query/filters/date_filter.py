"""Filter transactions by inclusive date range."""

from __future__ import annotations

from datetime import datetime

from memory.enriched_transaction import EnrichedTransaction


class DateFilter:
    def __init__(self, start: datetime | None = None, end: datetime | None = None):
        self.start, self.end = start, end
    def matches(self, item: EnrichedTransaction) -> bool:
        date = item.transaction.date
        return date is not None and (self.start is None or date >= self.start) and (self.end is None or date <= self.end)
