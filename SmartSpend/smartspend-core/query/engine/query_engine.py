"""Read-only query facade for Financial Memory."""

from dataclasses import replace
from time import perf_counter

from memory.memory_store import MemoryStore
from query.engine.optimizer import QueryOptimizer
from query.engine.planner import QueryPlanner
from query.engine.query_executor import QueryExecutor
from query.query import FinancialQuery
from query.query_result import QueryResult


class QueryEngine:
    """Validates, plans, and executes retrieval without interpreting results."""

    def __init__(self, memory: MemoryStore):
        self._memory = memory
        self._planner = QueryPlanner()
        self._optimizer = QueryOptimizer()
        self._executor = QueryExecutor()

    def execute(self, query: FinancialQuery) -> QueryResult:
        self._validate(query)
        start = perf_counter()
        plan = self._optimizer.optimize(self._planner.plan(query, self._memory))
        result = self._executor.execute(query, plan, 0.0)
        return replace(result, execution_time_ms=(perf_counter() - start) * 1000)

    @staticmethod
    def _validate(query: FinancialQuery) -> None:
        if query.limit is not None and query.limit < 1:
            raise ValueError("Query limit must be positive.")
        if query.sort_by is not None and not query.metrics:
            raise ValueError("Sorting requires an explicit metric.")
