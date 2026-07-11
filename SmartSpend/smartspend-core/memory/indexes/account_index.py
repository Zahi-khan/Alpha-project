"""Direct account-to-transaction lookup."""

from __future__ import annotations

from memory.events import TransactionProcessed
from memory.indexes._index import TransactionIndex


class AccountIndex(TransactionIndex):
    def key_for(self, event: TransactionProcessed) -> str | None:
        account = event.enriched_transaction.transaction.account
        return account.id if account is not None else None
