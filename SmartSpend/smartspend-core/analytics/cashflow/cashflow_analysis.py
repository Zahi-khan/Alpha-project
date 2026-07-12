"""Interpret net cash movement from a query result."""

from decimal import Decimal

from analytics.core.analytics_context import AnalyticsContext
from analytics.core.insight import FinancialInsight
from analytics.core.insight_type import InsightType


class CashFlowAnalysis:
    name = "cashflow"

    def analyze(self, context: AnalyticsContext) -> None:
        if any(row.group is not None for row in context.query_result.rows):
            return
        net = context.query_result.summary.get("sum")
        if not isinstance(net, Decimal):
            return
        positive = net >= 0
        context.add_insight(FinancialInsight(
            InsightType.CASH_FLOW,
            "Positive cash flow" if positive else "Negative cash flow",
            f"Net cash flow for the queried period is {net}.",
            severity="informational" if positive else "medium",
            confidence=1.0,
            supporting_evidence=("Derived from the query result's net sum.",),
            supporting_metrics={"net_cash_flow": net},
        ))
