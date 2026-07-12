"""Group financial events into income and expense flows."""


class TransactionTypeGrouping:
    def key_for(self, item):
        return item.transaction_type or ("income" if item.transaction.amount >= 0 else "expense")
