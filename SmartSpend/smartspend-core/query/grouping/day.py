"""Group by calendar day."""
class DayGrouping:
    def key_for(self, item):
        date = item.transaction.date
        return date.date().isoformat() if date else "Unknown"
