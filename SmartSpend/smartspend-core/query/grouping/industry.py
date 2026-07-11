"""Group by industry."""
class IndustryGrouping:
    def key_for(self, item): return item.industry.name if item.industry else "Unknown"
