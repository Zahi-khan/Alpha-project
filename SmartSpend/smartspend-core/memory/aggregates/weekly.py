"""Weekly transaction totals."""

from __future__ import annotations

from memory.aggregates._period import PeriodAggregate
from memory.events import TransactionProcessed


class WeeklyAggregate(PeriodAggregate):
    def key_for(self, event: TransactionProcessed) -> str | None:
        date = event.enriched_transaction.transaction.date
        return date.strftime("%G-W%V") if date is not None else None
