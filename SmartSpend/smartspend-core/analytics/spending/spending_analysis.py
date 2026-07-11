"""Identify the leading group in a grouped spending query."""

from decimal import Decimal

from analytics.core.analytics_context import AnalyticsContext
from analytics.core.insight import FinancialInsight
from analytics.core.insight_type import InsightType


class SpendingAnalysis:
    name = "spending"

    def analyze(self, context: AnalyticsContext) -> None:
        rows = [row for row in context.query_result.rows if isinstance(row.values.get("sum"), Decimal)]
        if not rows:
            return
        top = max(rows, key=lambda row: abs(row.values["sum"]))
        context.add_insight(FinancialInsight(
            InsightType.SPENDING,
            f"Largest spending group: {top.group}",
            f"{top.group} has the largest absolute total in this query.",
            confidence=1.0,
            supporting_evidence=(f"Grouped total: {top.values['sum']}.",),
            supporting_metrics=dict(top.values),
            metadata={"group": top.group},
        ))
