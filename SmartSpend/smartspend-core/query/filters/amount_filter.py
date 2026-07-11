"""Filter transactions by inclusive amount bounds."""

from __future__ import annotations

from decimal import Decimal

from memory.enriched_transaction import EnrichedTransaction


class AmountFilter:
    def __init__(self, minimum: Decimal | None = None, maximum: Decimal | None = None):
        self.minimum, self.maximum = minimum, maximum
    def matches(self, item: EnrichedTransaction) -> bool:
        amount = item.transaction.amount
        return (self.minimum is None or amount >= self.minimum) and (self.maximum is None or amount <= self.maximum)
