"""Group expenses by merchant and statement month for recurring-pattern analysis."""


class MerchantMonthGrouping:
    def key_for(self, item):
        merchant = item.merchant.canonical_name if item.merchant else item.transaction.description
        month = item.transaction.date.strftime("%Y-%m") if item.transaction.date else "unknown"
        return f"{merchant}|{month}"
