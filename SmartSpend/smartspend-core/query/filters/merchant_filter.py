"""Filter transactions by canonical merchant ID."""

from memory.enriched_transaction import EnrichedTransaction


class MerchantFilter:
    def __init__(self, merchant_id: str): self.merchant_id = merchant_id
    def matches(self, item: EnrichedTransaction) -> bool:
        merchant = item.merchant
        return merchant is not None and (merchant.id == self.merchant_id or merchant.canonical_name == self.merchant_id)
