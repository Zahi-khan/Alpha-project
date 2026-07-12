"""Group expenses by merchant, category, and month for recurring-cost analysis."""


class MerchantMonthCategoryGrouping:
    def key_for(self, item):
        merchant = item.merchant.canonical_name if item.merchant else item.transaction.description
        category = item.category.name if item.category else "Uncategorized"
        month = item.transaction.date.strftime("%Y-%m") if item.transaction.date else "unknown"
        return f"{merchant}|{category}|{month}"
