"""Yearly transaction totals."""

from __future__ import annotations

from memory.aggregates._period import PeriodAggregate
from memory.events import TransactionProcessed


class YearlyAggregate(PeriodAggregate):
    def key_for(self, event: TransactionProcessed) -> str | None:
        date = event.enriched_transaction.transaction.date
        return str(date.year) if date is not None else None
