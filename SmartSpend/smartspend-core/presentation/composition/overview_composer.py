"""Compose an immutable dashboard from application-owned verified outputs."""

from datetime import datetime
from decimal import Decimal

from presentation.formatting.currency_formatter import format_currency
from presentation.models.views import DashboardView, MetricCardView


class OverviewComposer:
    def compose(self, session_view, query_result, cashflow_result, insight_views, conclusions, charts, context):
        total = query_result.summary.get("sum", Decimal("0"))
        flows = {row.group: row.values.get("sum", Decimal("0")) for row in cashflow_result.rows}
        income = flows.get("income", Decimal("0"))
        expenses = abs(flows.get("expense", Decimal("0")))
        savings_rate = total / income * Decimal("100") if income > 0 else Decimal("0")
        cards = (
            MetricCardView("income", "Income", income, format_currency(income, context.currency), "Verified statement credits", "positive", "income"),
            MetricCardView("expenses", "Expenses", expenses, format_currency(expenses, context.currency), "Verified statement debits", "warning", "expenses"),
            MetricCardView("net_cash_flow", "Net cash flow", total, format_currency(total, context.currency), f"Across {query_result.summary.get('count', 0)} transactions", "positive" if total >= 0 else "warning", "cashflow"),
            MetricCardView("savings_rate", "Savings rate", savings_rate, f"{savings_rate:.1f}%", "Income remaining after expenses", "positive" if savings_rate >= 0 else "warning", "savings"),
        )
        imported = session_view.session_id and session_view.status != "failed"
        quality = {"parsed_rows": query_result.summary.get("count", 0), "warnings": (), "overall_status": "ready" if imported else "failed"}
        return DashboardView({"id": session_view.session_id, "status": session_view.status, "label": session_view.status_label, "expires_at": session_view.expires_at}, cards, tuple(insight_views), tuple(conclusions), tuple(charts), quality, datetime.utcnow())
