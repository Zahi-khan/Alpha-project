"""Shared query-filter protocol."""

from __future__ import annotations

from typing import Protocol

from memory.enriched_transaction import EnrichedTransaction


class TransactionFilter(Protocol):
    def matches(self, transaction: EnrichedTransaction) -> bool:
        """Return whether this one transaction satisfies the filter."""
