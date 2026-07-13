"""Assemble report data only; no PDF layout or financial calculation logic."""

from datetime import datetime

from application.reports.report_models import FinancialReport


class ReportBuilder:
    def build(self, session) -> FinancialReport:
        result = session.analysis_result
        dashboard = session.container.presentation_service.dashboard(session)
        return FinancialReport(
            generated_at=datetime.utcnow(),
            summary={
                "transaction_count": result.get("transaction_count", 0),
                "cash_flow": result.get("query", {}).get("summary", {}),
                "privacy_notice": "This temporary analysis is automatically deleted when the session expires.",
            },
            metrics=tuple(dashboard.get("summary_cards", ())),
            charts=tuple(dashboard.get("charts", ())),
            insights=tuple(result.get("insights", ())),
            conclusions=tuple(result.get("conclusions", ())),
            warnings=tuple(session.warnings),
        )
