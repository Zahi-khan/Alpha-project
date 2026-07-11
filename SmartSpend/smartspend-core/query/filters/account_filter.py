"""Filter transactions by account ID."""

from memory.enriched_transaction import EnrichedTransaction


class AccountFilter:
    def __init__(self, account_id: str): self.account_id = account_id
    def matches(self, item: EnrichedTransaction) -> bool:
        account = item.transaction.account
        return account is not None and account.id == self.account_id
