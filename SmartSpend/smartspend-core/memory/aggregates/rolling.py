"""On-demand rolling-window totals over chronological memory."""

from datetime import datetime, timedelta
from decimal import Decimal

from memory.history.transaction_history import TransactionHistory


class RollingAggregate:
    def __init__(self, history: TransactionHistory):
        self._history = history

    def total_for_days(self, days: int, end: datetime) -> Decimal:
        start = end - timedelta(days=days)
        return sum((item.transaction.amount for item in self._history.between(start, end)), Decimal("0.00"))
