"""Shared metric contract and amount extraction."""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable, Protocol

from memory.enriched_transaction import EnrichedTransaction


def amounts(items: Iterable[EnrichedTransaction]) -> list[Decimal]:
    return [item.transaction.amount for item in items]


class Metric(Protocol):
    name: str
    def calculate(self, items: Iterable[EnrichedTransaction]):
        """Calculate one value from a transaction collection."""
