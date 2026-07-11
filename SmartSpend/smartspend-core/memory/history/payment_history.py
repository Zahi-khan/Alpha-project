"""Facts observed for payment methods over time."""

from __future__ import annotations

from memory.events import TransactionProcessed
from memory.history._entity_history import EntityHistory


class PaymentHistory(EntityHistory):
    def key_for(self, event: TransactionProcessed) -> str | None:
        payment = event.enriched_transaction.payment
        return payment.method if payment is not None else None
