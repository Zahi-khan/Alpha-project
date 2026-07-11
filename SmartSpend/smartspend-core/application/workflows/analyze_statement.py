"""End-to-end anonymous statement analysis workflow."""

from application.dto.serializers import transaction_dto
from application.sessions.session_status import SessionStatus
from query.builder import FinancialQueryBuilder
from query.metrics.count import CountMetric
from query.metrics.sum import SumMetric


class AnalyzeStatementWorkflow:
    def analyze(self, session, file_bytes: bytes, filename: str) -> dict:
        session.status = SessionStatus.PROCESSING
        try:
            imported = session.container.statement_service.import_statement(file_bytes, filename)
            query = FinancialQueryBuilder().metric(SumMetric()).metric(CountMetric()).build()
            query_result = session.container.query_service.execute(query)
            insights = session.container.insight_service.generate(query, query_result)
            insight_objects = session.container.insight_service.objects()
            conclusions = session.container.reasoning_service.generate(insight_objects)
            session.analysis_result = {
                "import": imported,
                "transaction_count": imported["accepted_rows"],
                "query": {
                    "summary": dict(query_result.summary), "query_id": query.id,
                    "warnings": query_result.warnings,
                },
                "insights": insights,
                "conclusions": conclusions,
            }
            session.warnings.extend(imported["warnings"])
            session.status = SessionStatus.ANALYZED
            return session.analysis_result
        except Exception as error:
            session.status = SessionStatus.FAILED
            session.error = "Analysis could not be completed."
            raise
