"""Shared grouping contract."""

from __future__ import annotations

from typing import Protocol

from memory.enriched_transaction import EnrichedTransaction


class Grouping(Protocol):
    def key_for(self, transaction: EnrichedTransaction) -> str:
        """Return the output-group key for a transaction."""
