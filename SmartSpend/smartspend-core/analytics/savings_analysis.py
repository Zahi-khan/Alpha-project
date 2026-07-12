"""Explain savings capacity from verified income and expense totals."""

from decimal import Decimal

from analytics.core.analytics_context import AnalyticsContext
from intelligence.core.insight import FinancialInsight
from intelligence.core.insight_type import InsightType
from query.grouping.transaction_type import TransactionTypeGrouping


class SavingsAnalysis:
    name = "savings"

    def analyze(self, context: AnalyticsContext) -> None:
        if not isinstance(getattr(context.supporting_query, "group_by", None), TransactionTypeGrouping):
            return
        totals = {str(row.group): row.values.get("sum", Decimal("0")) for row in context.query_result.rows}
        income = totals.get("income", Decimal("0"))
        expenses = abs(totals.get("expense", Decimal("0")))
        if income <= 0:
            return
        savings = income - expenses
        savings_rate = savings / income * Decimal("100")
        context.add_insight(FinancialInsight(
            InsightType.FINANCIAL_HEALTH,
            "Savings capacity identified",
            f"Income of {income} and expenses of {expenses} left {savings} available across this statement period ({savings_rate:.1f}% savings rate).",
            severity="informational" if savings >= 0 else "medium",
            confidence=1.0,
            supporting_metrics={"income": income, "expenses": expenses, "savings": savings, "savings_rate": savings_rate},
            supporting_evidence=("Income and expense totals were calculated from the uploaded statement.",),
            tags=("savings",),
        ))
