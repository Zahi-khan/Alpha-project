"""Identify repeated merchant expenses across distinct statement months."""

from collections import defaultdict
from decimal import Decimal

from analytics.core.analytics_context import AnalyticsContext
from intelligence.core.insight import FinancialInsight
from intelligence.core.insight_type import InsightType
from query.grouping.merchant_month import MerchantMonthGrouping


class RecurringExpenseAnalysis:
    name = "recurring_expense"

    def analyze(self, context: AnalyticsContext) -> None:
        if not isinstance(getattr(context.supporting_query, "group_by", None), MerchantMonthGrouping):
            return
        grouped: dict[str, list[Decimal]] = defaultdict(list)
        for row in context.query_result.rows:
            if not row.group or "|" not in row.group or not isinstance(row.values.get("sum"), Decimal):
                continue
            merchant, _month = row.group.rsplit("|", 1)
            grouped[merchant].append(abs(row.values["sum"]))
        recurring = [(merchant, values) for merchant, values in grouped.items() if len(values) >= 2]
        if not recurring:
            return
        merchant, values = max(recurring, key=lambda candidate: sum(candidate[1], Decimal("0")))
        total = sum(values, Decimal("0"))
        average = total / len(values)
        context.add_insight(FinancialInsight(
            InsightType.RECURRING,
            f"Most prominent recurring expense: {merchant}",
            f"{merchant} appeared in {len(values)} statement months, with {total} spent in total and about {average} per month on average.",
            severity="informational",
            confidence=0.88,
            supporting_metrics={"recurring_total": total, "average_monthly_cost": average, "months_observed": len(values)},
            supporting_evidence=(f"The same merchant appeared in {len(values)} distinct statement months.",),
            tags=("recurring",),
        ))
