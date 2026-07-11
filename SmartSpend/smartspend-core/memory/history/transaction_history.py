"""Chronological transaction memory with range and account queries."""

from datetime import datetime

from memory.enriched_transaction import EnrichedTransaction
from memory.events import TransactionProcessed


class TransactionHistory:
    def __init__(self):
        self.transactions: list[EnrichedTransaction] = []

    def handle(self, event: TransactionProcessed) -> None:
        self.transactions.append(event.enriched_transaction)
        self.transactions.sort(key=lambda item: item.transaction.date or datetime.min)

    def between(self, start: datetime, end: datetime) -> list[EnrichedTransaction]:
        return [
            item
            for item in self.transactions
            if item.transaction.date is not None and start <= item.transaction.date <= end
        ]

    def for_account(self, account_id: str) -> list[EnrichedTransaction]:
        return [
            item
            for item in self.transactions
            if item.transaction.account is not None and item.transaction.account.id == account_id
        ]
