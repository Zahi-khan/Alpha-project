"""Application workflow from stored insights to immutable conclusions."""

from application.dto.serializers import conclusion_dto
from intelligence.core.insight import FinancialInsight
from reasoning.engine import ReasoningEngine
from reasoning.explainability_graph import ExplainabilityGraph


class ReasoningService:
    def __init__(self, engine: ReasoningEngine, graph: ExplainabilityGraph):
        self._engine, self._graph = engine, graph
        self._conclusions: dict[str, object] = {}

    def generate(self, insights: tuple[FinancialInsight, ...]) -> list[dict]:
        conclusions = self._engine.reason(insights)
        for conclusion in conclusions:
            self._conclusions[conclusion.id] = conclusion
            self._graph.add_conclusion(conclusion)
        return [conclusion_dto(item) for item in conclusions]

    def list(self) -> list[dict]: return [conclusion_dto(item) for item in self._conclusions.values()]
    def objects(self) -> tuple: return tuple(self._conclusions.values())
