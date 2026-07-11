"""Versioned in-memory snapshots with trusted-local serialization support."""

from __future__ import annotations

from datetime import datetime
from pickle import dumps, loads

from memory.enriched_transaction import EnrichedTransaction
from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class Snapshot:
    version: int
    created_at: datetime
    transactions: tuple[EnrichedTransaction, ...]

    @classmethod
    def from_store(cls, store) -> Snapshot:
        return cls(1, datetime.utcnow(), tuple(store.transactions))

    def restore(self):
        from memory.memory_store import MemoryStore

        store = MemoryStore()
        for transaction in self.transactions:
            store.process(transaction)
        return store

    def serialize(self) -> bytes:
        """Serialize only trusted local snapshots; pickle is not untrusted input safe."""
        return dumps(self)

    @classmethod
    def deserialize(cls, payload: bytes) -> Snapshot:
        snapshot = loads(payload)
        if not isinstance(snapshot, cls):
            raise ValueError("Snapshot payload has an unexpected type.")
        return snapshot
