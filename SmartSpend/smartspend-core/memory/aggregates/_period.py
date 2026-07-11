"""Shared period aggregate implementation."""

from __future__ import annotations

from decimal import Decimal

from memory.events import TransactionProcessed


class PeriodAggregate:
    def __init__(self):
        self.totals: dict[str, Decimal] = {}
        self.counts: dict[str, int] = {}

    def handle(self, event: TransactionProcessed) -> None:
        key = self.key_for(event)
        if key is None:
            return
        amount = event.enriched_transaction.transaction.amount
        self.totals[key] = self.totals.get(key, Decimal("0.00")) + amount
        self.counts[key] = self.counts.get(key, 0) + 1

    def key_for(self, event: TransactionProcessed) -> str | None:
        raise NotImplementedError
