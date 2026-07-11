"""Group by merchant."""
class MerchantGrouping:
    def key_for(self, item):
        return item.merchant.canonical_name if item.merchant else "Unresolved"
