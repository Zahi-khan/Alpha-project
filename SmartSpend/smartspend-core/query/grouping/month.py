"""Group by calendar month."""
class MonthGrouping:
    def key_for(self, item):
        date = item.transaction.date
        return date.strftime("%Y-%m") if date else "Unknown"
