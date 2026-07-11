"""Event-driven long-term financial memory; no analytics or recommendations."""

from collections.abc import Callable

from memory.aggregates.monthly import MonthlyAggregate
from memory.aggregates.yearly import YearlyAggregate
from memory.aggregates.weekly import WeeklyAggregate
from memory.enriched_transaction import EnrichedTransaction
from memory.events import TransactionProcessed
from memory.history.account_history import AccountHistory
from memory.history.category_history import CategoryHistory
from memory.history.industry_history import IndustryHistory
from memory.history.merchant_history import MerchantHistory
from memory.history.payment_history import PaymentHistory
from memory.history.transaction_history import TransactionHistory
from memory.indexes.account_index import AccountIndex
from memory.indexes.category_index import CategoryIndex
from memory.indexes.date_index import DateIndex
from memory.indexes.merchant_index import MerchantIndex


class MemoryStore:
    """Stores enriched records and broadcasts events to independent subscribers."""

    def __init__(self):
        self.transactions: list[EnrichedTransaction] = []
        self.transaction_history = TransactionHistory()
        self.merchant_history = MerchantHistory()
        self.category_history = CategoryHistory()
        self.account_history = AccountHistory()
        self.payment_history = PaymentHistory()
        self.industry_history = IndustryHistory()
        self.merchant_index = MerchantIndex()
        self.category_index = CategoryIndex()
        self.account_index = AccountIndex()
        self.date_index = DateIndex()
        self.monthly = MonthlyAggregate()
        self.weekly = WeeklyAggregate()
        self.yearly = YearlyAggregate()
        self._subscribers: list[Callable[[TransactionProcessed], None]] = []
        for subscriber in (
            self.transaction_history,
            self.merchant_history,
            self.category_history,
            self.account_history,
            self.payment_history,
            self.industry_history,
            self.merchant_index,
            self.category_index,
            self.account_index,
            self.date_index,
            self.monthly,
            self.weekly,
            self.yearly,
        ):
            self.subscribe(subscriber.handle)

    def subscribe(self, handler: Callable[[TransactionProcessed], None]) -> None:
        self._subscribers.append(handler)

    def process(self, enriched_transaction: EnrichedTransaction) -> None:
        self.transactions.append(enriched_transaction)
        event = TransactionProcessed(enriched_transaction)
        for handler in tuple(self._subscribers):
            handler(event)

    def find_by_merchant(self, merchant_id: str) -> tuple[EnrichedTransaction, ...]:
        return self.merchant_index.find(merchant_id)

    def clear(self) -> None:
        """Discard all session-owned financial memory and derived indexes."""
        self.__init__()
