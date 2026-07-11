"""Build and write the temporary report for a completed analysis session."""

from __future__ import annotations

from application.reports.pdf_generator import PDFGenerator
from application.reports.report_builder import ReportBuilder
from application.sessions.session_status import SessionStatus


class GenerateReportWorkflow:
    def __init__(self, builder: ReportBuilder | None = None, generator: PDFGenerator | None = None):
        self._builder, self._generator = builder or ReportBuilder(), generator or PDFGenerator()

    def generate(self, session):
        if session.status not in (SessionStatus.ANALYZED, SessionStatus.REPORT_READY):
            raise ValueError("A completed analysis is required before generating a report.")
        report = self._builder.build(session)
        session.report_path = self._generator.generate(report, session.root_path / "report" / "financial_overview.pdf")
        session.status = SessionStatus.REPORT_READY
        return session.report_path
