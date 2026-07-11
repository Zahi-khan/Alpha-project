"""Interpret change between first and last ordered grouped totals."""

from decimal import Decimal

from analytics.core.analytics_context import AnalyticsContext
from analytics.core.baselines import BaselineService
from analytics.core.insight import FinancialInsight
from analytics.core.insight_type import InsightType


class TrendAnalysis:
    name = "trends"

    def analyze(self, context: AnalyticsContext) -> None:
        rows = [row for row in context.query_result.rows if isinstance(row.values.get("sum"), Decimal)]
        if len(rows) < 2:
            return
        first, last = rows[0], rows[-1]
        change = BaselineService.percent_change(abs(last.values["sum"]), abs(first.values["sum"]))
        if change is None:
            return
        direction = "increased" if change > 0 else "decreased" if change < 0 else "remained stable"
        context.add_insight(FinancialInsight(
            InsightType.TREND,
            f"Spending {direction}",
            f"Grouped spending changed by {abs(change):.1f}% from {first.group} to {last.group}.",
            severity="medium" if abs(change) >= 20 else "informational",
            confidence=0.85,
            supporting_evidence=(f"{first.group}: {first.values['sum']}; {last.group}: {last.values['sum']}.",),
            supporting_metrics={"percent_change": change},
        ))
