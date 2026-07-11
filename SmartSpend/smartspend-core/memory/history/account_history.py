"""Facts observed for financial accounts over time."""

from __future__ import annotations

from decimal import Decimal

from memory.events import TransactionProcessed
from memory.history._entity_history import EntityHistory


class AccountHistory(EntityHistory):
    def __init__(self):
        super().__init__()
        self.money_in: dict[str, Decimal] = {}
        self.money_out: dict[str, Decimal] = {}

    def key_for(self, event: TransactionProcessed) -> str | None:
        account = event.enriched_transaction.transaction.account
        return account.id if account is not None else None

    def handle(self, event: TransactionProcessed) -> None:
        key = self.key_for(event)
        if key is None:
            return
        super().handle(event)
        amount = event.enriched_transaction.transaction.amount
        target = self.money_in if amount > 0 else self.money_out
        target[key] = target.get(key, Decimal("0.00")) + abs(amount)
