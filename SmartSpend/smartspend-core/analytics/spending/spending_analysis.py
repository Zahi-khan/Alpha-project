"""Identify the leading group in a grouped spending query."""

from decimal import Decimal

from analytics.core.analytics_context import AnalyticsContext
from analytics.core.insight import FinancialInsight
from analytics.core.insight_type import InsightType
from query.grouping.category import CategoryGrouping
from query.grouping.merchant import MerchantGrouping


class SpendingAnalysis:
    name = "spending"

    def analyze(self, context: AnalyticsContext) -> None:
        grouping = getattr(context.supporting_query, "group_by", None)
        if not isinstance(grouping, (CategoryGrouping, MerchantGrouping)):
            return
        rows = [row for row in context.query_result.rows if row.group is not None and isinstance(row.values.get("sum"), Decimal)]
        if not rows:
            return
        top = max(rows, key=lambda row: abs(row.values["sum"]))
        context.add_insight(FinancialInsight(
            InsightType.SPENDING,
            f"{'Largest spending category' if isinstance(grouping, CategoryGrouping) else 'Top merchant by spending'}: {top.group}",
            f"{top.group} has the largest verified expense total in this statement period.",
            confidence=1.0,
            supporting_evidence=(f"Grouped total: {top.values['sum']}.",),
            supporting_metrics=dict(top.values),
            metadata={"group": top.group},
        ))
