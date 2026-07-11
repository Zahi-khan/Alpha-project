"""Group by category."""
class CategoryGrouping:
    def key_for(self, item): return item.category.name if item.category else "Uncategorized"
