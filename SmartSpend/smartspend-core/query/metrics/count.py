"""Count metric."""
class CountMetric:
    name = "count"
    def calculate(self, items): return len(list(items))
