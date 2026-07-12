"""Suggest a bounded, explainable reduction in the largest expense category."""

from decimal import Decimal

from analytics.core.analytics_context import AnalyticsContext
from intelligence.core.insight import FinancialInsight
from intelligence.core.insight_type import InsightType
from query.grouping.category import CategoryGrouping


class SavingsOpportunityAnalysis:
    name = "savings_opportunity"

    def analyze(self, context: AnalyticsContext) -> None:
        if not isinstance(getattr(context.supporting_query, "group_by", None), CategoryGrouping):
            return
        rows = [row for row in context.query_result.rows if row.group and isinstance(row.values.get("sum"), Decimal)]
        if not rows:
            return
        top = min(rows, key=lambda row: row.values["sum"])
        expense = abs(top.values["sum"])
        potential = expense * Decimal("0.10")
        context.add_insight(FinancialInsight(
            InsightType.SAVINGS,
            f"A place to cut back: {top.group}",
            f"You spent {expense} on {top.group}. Reducing this category by 10% could free about {potential} over a similar statement period.",
            severity="informational",
            confidence=0.90,
            supporting_metrics={"category_expense": expense, "potential_savings": potential, "reduction_rate": Decimal("10")},
            supporting_evidence=(f"{top.group} was the largest verified expense category.",),
            tags=("savings", str(top.group).casefold().replace(" ", "_")),
        ))
