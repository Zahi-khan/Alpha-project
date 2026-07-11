"""Simple rolling average over the latest N values in query order."""
from decimal import Decimal
from query.metrics._base import amounts
class RollingAverageMetric:
    def __init__(self, window: int):
        if window < 1: raise ValueError("Rolling window must be positive.")
        self.window, self.name = window, f"rolling_average_{window}"
    def calculate(self, items):
        values = amounts(items)[-self.window:]
        return sum(values, Decimal("0.00")) / len(values) if values else Decimal("0.00")
