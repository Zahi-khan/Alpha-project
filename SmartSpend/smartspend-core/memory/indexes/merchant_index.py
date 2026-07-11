"""Direct merchant-to-transaction lookup."""

from __future__ import annotations

from memory.events import TransactionProcessed
from memory.indexes._index import TransactionIndex


class MerchantIndex(TransactionIndex):
    def key_for(self, event: TransactionProcessed) -> str | None:
        merchant = event.enriched_transaction.merchant
        return merchant.id or merchant.canonical_name if merchant is not None else None
