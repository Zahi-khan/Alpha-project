"""Shared direct-access index implementation."""

from __future__ import annotations

from memory.enriched_transaction import EnrichedTransaction
from memory.events import TransactionProcessed


class TransactionIndex:
    def __init__(self):
        self.entries: dict[str, list[EnrichedTransaction]] = {}

    def handle(self, event: TransactionProcessed) -> None:
        key = self.key_for(event)
        if key is not None:
            self.entries.setdefault(key, []).append(event.enriched_transaction)

    def find(self, key: str) -> tuple[EnrichedTransaction, ...]:
        return tuple(self.entries.get(key, ()))

    def key_for(self, event: TransactionProcessed) -> str | None:
        raise NotImplementedError
