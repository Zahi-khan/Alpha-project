"""Composition root: builds the application once, components never import it."""

from application.services.explainability_service import ExplainabilityService
from application.services.goal_service import GoalService
from application.services.insight_service import InsightService
from application.services.planning_service import PlanningService
from application.services.presentation_service import PresentationService
from application.services.query_service import QueryService
from application.services.reasoning_service import ReasoningService
from application.services.statement_service import StatementService
from application.services.transaction_service import TransactionService
from intelligence.defaults import build_default_intelligence_registry
from intelligence.enrichment import build_enrichment_pipeline
from intelligence.core.intelligence_engine import FinancialIntelligenceEngine
from knowledge.knowledge_base import KnowledgeBase
from memory.memory_store import MemoryStore
from planning.planning_engine import PlanningEngine
from query.engine.query_engine import QueryEngine
from reasoning.defaults import build_default_reasoning_registry
from reasoning.engine import ReasoningEngine
from reasoning.explainability_graph import ExplainabilityGraph


class ApplicationContainer:
    def __init__(self):
        self.knowledge_base = KnowledgeBase.from_json()
        self.enrichment_pipeline = build_enrichment_pipeline(self.knowledge_base)
        self.memory_store = MemoryStore()
        self.query_engine = QueryEngine(self.memory_store)
        self.intelligence_engine = FinancialIntelligenceEngine(build_default_intelligence_registry())
        self.reasoning_engine = ReasoningEngine(build_default_reasoning_registry())
        self.planning_engine = PlanningEngine()
        self.explainability_graph = ExplainabilityGraph()

        self.statement_service = StatementService(self.enrichment_pipeline, self.memory_store, self.explainability_graph)
        self.transaction_service = TransactionService(self.memory_store, self.query_engine)
        self.query_service = QueryService(self.query_engine)
        self.insight_service = InsightService(self.intelligence_engine, self.explainability_graph)
        self.reasoning_service = ReasoningService(self.reasoning_engine, self.explainability_graph)
        self.goal_service = GoalService()
        self.planning_service = PlanningService(self.goal_service, self.planning_engine)
        self.explainability_service = ExplainabilityService(self.explainability_graph)
        self.presentation_service = PresentationService()
