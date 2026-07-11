"""Shared factual observation tracking for memory histories."""

from __future__ import annotations

from dataclasses import field
from datetime import datetime
from decimal import Decimal

from memory.events import TransactionProcessed
from models._dataclasses import slotted_dataclass


@slotted_dataclass
class EntityObservation:
    transaction_count: int = 0
    total_amount: Decimal = Decimal("0.00")
    first_transaction: datetime | None = None
    last_transaction: datetime | None = None
    smallest_amount: Decimal | None = None
    largest_amount: Decimal | None = None

    @property
    def average_amount(self) -> Decimal:
        if not self.transaction_count:
            return Decimal("0.00")
        return self.total_amount / self.transaction_count

    def record(self, event: TransactionProcessed) -> None:
        transaction = event.enriched_transaction.transaction
        self.transaction_count += 1
        self.total_amount += transaction.amount
        if transaction.date is not None:
            if self.first_transaction is None or transaction.date < self.first_transaction:
                self.first_transaction = transaction.date
            if self.last_transaction is None or transaction.date > self.last_transaction:
                self.last_transaction = transaction.date
        if self.smallest_amount is None or transaction.amount < self.smallest_amount:
            self.smallest_amount = transaction.amount
        if self.largest_amount is None or transaction.amount > self.largest_amount:
            self.largest_amount = transaction.amount


class EntityHistory:
    """Base event subscriber keyed by one resolved transaction dimension."""

    def __init__(self):
        self.observations: dict[str, EntityObservation] = {}

    def handle(self, event: TransactionProcessed) -> None:
        key = self.key_for(event)
        if key is None:
            return
        self.observations.setdefault(key, EntityObservation()).record(event)

    def key_for(self, event: TransactionProcessed) -> str | None:
        raise NotImplementedError
