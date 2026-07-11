"""Application-facing presentation composition with no direct core leakage."""

from dataclasses import asdict

from presentation.core.presentation_context import PresentationContext
from presentation.core.presentation_engine import PresentationEngine
from query.builder import FinancialQueryBuilder
from query.grouping.month import MonthGrouping
from query.metrics.count import CountMetric
from query.metrics.sum import SumMetric


class PresentationService:
    def __init__(self):
        self._engine = PresentationEngine()

    def dashboard(self, session) -> dict:
        context = PresentationContext(session_id=session.session_id)
        query = FinancialQueryBuilder().group(MonthGrouping()).metric(SumMetric()).metric(CountMetric()).build()
        result = session.container.query_service.execute(query)
        view = self._engine.build_dashboard(
            session, result, session.container.insight_service.objects(),
            session.container.reasoning_service.objects(), context,
        )
        return asdict(view)

    def transactions(self, session) -> dict:
        context = PresentationContext(session_id=session.session_id)
        return {"data": [asdict(view) for view in self._engine.build_transaction_list(session.container.memory_store.transactions, context)]}

    def insights(self, session) -> dict:
        context = PresentationContext(session_id=session.session_id)
        return {"data": [asdict(view) for view in self._engine.build_insight_feed(session.container.insight_service.objects(), context)]}

    def explanation(self, session, root_id: str) -> dict:
        context = PresentationContext(session_id=session.session_id)
        return asdict(self._engine.build_explanation(session.container.explainability_service.trace(root_id), context))
