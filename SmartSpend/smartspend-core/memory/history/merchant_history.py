"""Facts observed from interactions with individual merchants."""

from __future__ import annotations

from memory.events import TransactionProcessed
from memory.history._entity_history import EntityHistory


class MerchantHistory(EntityHistory):
    def key_for(self, event: TransactionProcessed) -> str | None:
        merchant = event.enriched_transaction.merchant
        return merchant.id or merchant.canonical_name if merchant is not None else None
