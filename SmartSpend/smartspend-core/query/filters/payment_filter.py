"""Filter transactions by resolved payment method."""

from memory.enriched_transaction import EnrichedTransaction


class PaymentFilter:
    def __init__(self, method: str): self.method = method
    def matches(self, item: EnrichedTransaction) -> bool:
        return item.payment is not None and item.payment.method == self.method
