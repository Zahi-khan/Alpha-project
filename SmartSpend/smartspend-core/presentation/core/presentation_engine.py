"""Coordinates focused presenters; it never performs financial interpretation."""

from presentation.charts.chart_factory import ChartFactory
from presentation.composition.overview_composer import OverviewComposer
from presentation.presenters.explainability_presenter import ExplainabilityPresenter
from presentation.presenters.insight_presenter import InsightPresenter
from presentation.presenters.session_presenter import SessionPresenter
from presentation.presenters.transaction_presenter import TransactionPresenter


class PresentationEngine:
    def __init__(self):
        self._insights = InsightPresenter(); self._transactions = TransactionPresenter(); self._sessions = SessionPresenter(); self._explanations = ExplainabilityPresenter(); self._charts = ChartFactory(); self._overview = OverviewComposer()
    def build_transaction_list(self, transactions, context): return tuple(self._transactions.present(item, context) for item in transactions)
    def build_insight_feed(self, insights, context): return tuple(self._insights.present(item, context) for item in insights)
    def build_explanation(self, trace, context): return self._explanations.present(trace, context)
    def build_dashboard(self, session, query_result, insights, conclusions, context):
        session_view = self._sessions.present(session, context)
        insight_views = self.build_insight_feed(insights, context)
        chart = self._charts.from_query_result(query_result, "cashflow", "Financial overview")
        return self._overview.compose(session_view, query_result, insight_views, conclusions, chart, context)
