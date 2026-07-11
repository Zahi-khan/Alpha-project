"""Group by account."""
class AccountGrouping:
    def key_for(self, item):
        account = item.transaction.account
        return account.display_name if account else "Unassigned"
