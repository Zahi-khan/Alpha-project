"""Coordinates Financial Intelligence capabilities into traceable insights."""

from application.dto.serializers import insight_dto
from intelligence.core.intelligence_context import IntelligenceContext
from intelligence.core.intelligence_engine import FinancialIntelligenceEngine
from query.query import FinancialQuery
from query.query_result import QueryResult
from reasoning.explainability_graph import ExplainabilityGraph


class InsightService:
    def __init__(self, engine: FinancialIntelligenceEngine, graph: ExplainabilityGraph):
        self._engine, self._graph = engine, graph
        self._insights: dict[str, object] = {}

    def generate(self, query: FinancialQuery, result: QueryResult) -> list[dict]:
        self._graph.add_query(query, result)
        insights = self._engine.evaluate(IntelligenceContext(query_result=result, supporting_query=query))
        for insight in insights:
            self._insights[insight.id] = insight
            self._graph.add_insight(insight)
        return [insight_dto(item) for item in insights]

    def get(self, insight_id: str): return self._insights.get(insight_id)
    def list(self) -> list[dict]: return [insight_dto(item) for item in self._insights.values()]
    def objects(self) -> tuple: return tuple(self._insights.values())
