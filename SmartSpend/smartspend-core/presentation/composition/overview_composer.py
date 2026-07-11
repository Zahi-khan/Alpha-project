"""Compose an immutable dashboard from application-owned verified outputs."""

from datetime import datetime
from decimal import Decimal

from presentation.formatting.currency_formatter import format_currency
from presentation.models.views import DashboardView, MetricCardView


class OverviewComposer:
    def compose(self, session_view, query_result, insight_views, conclusions, chart, context):
        total = query_result.summary.get("sum", Decimal("0"))
        cards = (MetricCardView("net_cash_flow", "Net cash flow", total, format_currency(total, context.currency), f"Across {query_result.summary.get('count', 0)} transactions", "positive" if total >= 0 else "warning", "cashflow"),)
        quality = {"parsed_rows": session_view.session_id and session_view.status != "failed", "warnings": (), "overall_status": "ready"}
        return DashboardView({"id": session_view.session_id, "status": session_view.status, "label": session_view.status_label, "expires_at": session_view.expires_at}, cards, tuple(insight_views), tuple(conclusions), (chart,), quality, datetime.utcnow())
