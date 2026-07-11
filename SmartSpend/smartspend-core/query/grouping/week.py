"""Group by ISO week."""
class WeekGrouping:
    def key_for(self, item):
        date = item.transaction.date
        return date.strftime("%G-W%V") if date else "Unknown"
