"""Select a memory index when a query contains an indexable filter."""

from __future__ import annotations

from dataclasses import dataclass

from memory.enriched_transaction import EnrichedTransaction
from memory.memory_store import MemoryStore
from query.filters.account_filter import AccountFilter
from query.filters.category_filter import CategoryFilter
from query.filters.merchant_filter import MerchantFilter
from query.query import FinancialQuery


@dataclass(frozen=True)
class QueryPlan:
    seed: tuple[EnrichedTransaction, ...]
    index_used: str | None = None


class QueryPlanner:
    def plan(self, query: FinancialQuery, memory: MemoryStore) -> QueryPlan:
        candidates: list[QueryPlan] = []
        for filter_ in query.filters:
            if isinstance(filter_, MerchantFilter):
                candidates.append(QueryPlan(memory.merchant_index.find(filter_.merchant_id), "merchant"))
            elif isinstance(filter_, CategoryFilter):
                candidates.append(QueryPlan(memory.category_index.find(filter_.category_id), "category"))
            elif isinstance(filter_, AccountFilter):
                candidates.append(QueryPlan(memory.account_index.find(filter_.account_id), "account"))
        if candidates:
            return min(candidates, key=lambda plan: len(plan.seed))
        return QueryPlan(tuple(memory.transactions))
