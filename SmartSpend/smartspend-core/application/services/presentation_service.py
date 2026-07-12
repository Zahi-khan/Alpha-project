"""Application-facing presentation composition with no direct core leakage."""

from dataclasses import asdict
from decimal import Decimal

from presentation.core.presentation_context import PresentationContext
from presentation.core.presentation_engine import PresentationEngine
from query.builder import FinancialQueryBuilder
from query.grouping.month import MonthGrouping
from query.grouping.category import CategoryGrouping
from query.grouping.merchant import MerchantGrouping
from query.grouping.payment import PaymentGrouping
from query.grouping.transaction_type import TransactionTypeGrouping
from query.filters.amount_filter import AmountFilter
from query.metrics.count import CountMetric
from query.metrics.sum import SumMetric


class PresentationService:
    def __init__(self):
        self._engine = PresentationEngine()

    def dashboard(self, session) -> dict:
        context = PresentationContext(session_id=session.session_id)
        summary_query = FinancialQueryBuilder().metric(SumMetric()).metric(CountMetric()).build()
        summary = session.container.query_service.execute(summary_query)
        cashflow = session.container.query_service.execute(FinancialQueryBuilder().group(TransactionTypeGrouping()).metric(SumMetric()).metric(CountMetric()).build())
        monthly = session.container.query_service.execute(FinancialQueryBuilder().group(MonthGrouping()).metric(SumMetric()).metric(CountMetric()).build())
        expense_only = AmountFilter(maximum=Decimal("-0.01"))
        categories = session.container.query_service.execute(FinancialQueryBuilder().where(expense_only).group(CategoryGrouping()).metric(SumMetric()).metric(CountMetric()).build())
        merchants = session.container.query_service.execute(FinancialQueryBuilder().where(expense_only).group(MerchantGrouping()).metric(SumMetric()).metric(CountMetric()).build())
        payments = session.container.query_service.execute(FinancialQueryBuilder().where(expense_only).group(PaymentGrouping()).metric(SumMetric()).metric(CountMetric()).build())
        charts = (
            self._engine.build_chart(monthly, "monthly_cashflow", "Monthly cash flow", "line"),
            self._engine.build_chart(categories, "category_spending", "Spending by category", "bar"),
            self._engine.build_chart(merchants, "merchant_spending", "Top merchants", "bar"),
            self._engine.build_chart(payments, "payment_methods", "Payment methods", "bar"),
        )
        view = self._engine.build_dashboard(
            session, summary, cashflow, session.container.insight_service.objects(),
            session.container.reasoning_service.objects(), context, charts,
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
