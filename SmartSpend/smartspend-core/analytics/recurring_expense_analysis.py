"""Identify repeated merchant expenses across distinct statement months."""

from collections import defaultdict
from decimal import Decimal

from analytics.core.analytics_context import AnalyticsContext
from intelligence.core.insight import FinancialInsight
from intelligence.core.insight_type import InsightType
from query.grouping.merchant_month import MerchantMonthGrouping
from query.grouping.merchant_month_category import MerchantMonthCategoryGrouping
from analytics.spending_policy import is_essential_category


class RecurringExpenseAnalysis:
    name = "recurring_expense"

    def analyze(self, context: AnalyticsContext) -> None:
        if not isinstance(getattr(context.supporting_query, "group_by", None), MerchantMonthCategoryGrouping):
            return
        grouped: dict[tuple[str, str], list[Decimal]] = defaultdict(list)
        for row in context.query_result.rows:
            if not row.group or row.group.count("|") < 2 or not isinstance(row.values.get("sum"), Decimal):
                continue
            merchant, category, _month = row.group.rsplit("|", 2)
            if not is_essential_category(category):
                grouped[(merchant, category)].append(abs(row.values["sum"]))
        recurring = [(merchant, category, values) for (merchant, category), values in grouped.items() if len(values) >= 2]
        if not recurring:
            return
        merchant, category, values = max(recurring, key=lambda candidate: sum(candidate[2], Decimal("0")))
        total = sum(values, Decimal("0"))
        average = total / len(values)
        context.add_insight(FinancialInsight(
            InsightType.RECURRING,
            f"Most prominent recurring discretionary expense: {merchant}",
            f"{merchant} appeared in {len(values)} statement months in {category}, with {total} spent in total and about {average} per month on average.",
            severity="informational",
            confidence=0.88,
            supporting_metrics={"recurring_total": total, "average_monthly_cost": average, "months_observed": len(values)},
            supporting_evidence=(f"The same merchant appeared in {len(values)} distinct statement months.",),
            tags=("recurring",),
        ))
