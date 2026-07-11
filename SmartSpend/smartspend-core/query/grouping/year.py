"""Group by calendar year."""
class YearGrouping:
    def key_for(self, item):
        date = item.transaction.date
        return str(date.year) if date else "Unknown"
