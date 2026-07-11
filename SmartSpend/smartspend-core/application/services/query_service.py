"""Validated application access to the read-only Financial Query Engine."""

from query.engine.query_engine import QueryEngine
from query.query import FinancialQuery


class QueryService:
    def __init__(self, engine: QueryEngine): self._engine = engine
    def execute(self, query: FinancialQuery): return self._engine.execute(query)
