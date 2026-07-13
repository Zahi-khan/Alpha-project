from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from pypdf import PdfReader

from application.container import ApplicationContainer
from application.reports.pdf_generator import PDFGenerator
from application.reports.report_builder import ReportBuilder
from application.sessions.analysis_session import AnalysisSession
from application.workflows.analyze_statement import AnalyzeStatementWorkflow


class FinancialSummaryPdfTests(unittest.TestCase):
    def test_report_has_spaced_summary_and_relevant_charts(self):
        with TemporaryDirectory() as root:
            root_path = Path(root)
            session = AnalysisSession(
                "report_test",
                datetime.utcnow(),
                datetime.utcnow() + timedelta(hours=1),
                root_path,
                ApplicationContainer(),
            )
            sample = Path(__file__).parents[1] / "data" / "sample_transactions.csv"
            AnalyzeStatementWorkflow().analyze(session, sample.read_bytes(), sample.name)
            report = ReportBuilder().build(session)
            output = PDFGenerator().generate(report, root_path / "summary.pdf")

            reader = PdfReader(output)
            extracted = "\n".join(page.extract_text() or "" for page in reader.pages)

            self.assertEqual(4, len(report.metrics))
            self.assertGreaterEqual(len(report.charts), 2)
            self.assertIn("Cash-flow overview", extracted)
            self.assertIn("Spending by category", extracted)
            self.assertIn("Monthly cash flow", extracted)
            self.assertIn("PDF passwords", extracted)
            self.assertNotIn("bank-secret", extracted)


if __name__ == "__main__":
    unittest.main()
