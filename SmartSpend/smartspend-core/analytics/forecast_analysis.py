"""Conservative, explainable cash-flow projection from completed statement months."""

from decimal import Decimal

from analytics.core.analytics_context import AnalyticsContext
from intelligence.core.insight import FinancialInsight
from intelligence.core.insight_type import InsightType
from query.grouping.month import MonthGrouping


class ForecastAnalysis:
    name = "forecast"

    def analyze(self, context: AnalyticsContext) -> None:
        if not isinstance(getattr(context.supporting_query, "group_by", None), MonthGrouping):
            return
        values = [row.values.get("sum") for row in context.query_result.rows if isinstance(row.values.get("sum"), Decimal)]
        if len(values) < 2:
            return
        projected_net = sum(values, Decimal("0")) / len(values)
        confidence = min(0.80, 0.50 + len(values) * 0.05)
        context.add_insight(FinancialInsight(
            InsightType.FORECAST,
            "Projected next-month net cash flow",
            f"Based on the average net cash flow across {len(values)} statement months, the next month may end near {projected_net}. This is a projection, not a guarantee.",
            severity="informational" if projected_net >= 0 else "medium",
            confidence=confidence,
            supporting_metrics={"projected_net": projected_net, "months_observed": len(values)},
            supporting_evidence=(f"Average calculated from {len(values)} completed monthly totals.",),
            tags=("forecast",),
        ))
