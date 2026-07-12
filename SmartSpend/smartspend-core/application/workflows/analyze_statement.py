"""End-to-end anonymous statement analysis workflow."""

from application.dto.serializers import transaction_dto
from application.sessions.session_status import SessionStatus
from query.builder import FinancialQueryBuilder
from query.grouping.category import CategoryGrouping
from query.grouping.merchant import MerchantGrouping
from query.grouping.month import MonthGrouping
from query.metrics.count import CountMetric
from query.metrics.sum import SumMetric


class AnalyzeStatementWorkflow:
    def analyze(self, session, file_bytes: bytes, filename: str) -> dict:
        session.status = SessionStatus.PROCESSING
        try:
            imported = session.container.statement_service.import_statement(file_bytes, filename)
            queries = (
                FinancialQueryBuilder().metric(SumMetric()).metric(CountMetric()).build(),
                FinancialQueryBuilder().group(MonthGrouping()).metric(SumMetric()).metric(CountMetric()).build(),
                FinancialQueryBuilder().group(CategoryGrouping()).metric(SumMetric()).metric(CountMetric()).build(),
                FinancialQueryBuilder().group(MerchantGrouping()).metric(SumMetric()).metric(CountMetric()).build(),
            )
            query_results = [session.container.query_service.execute(query) for query in queries]
            insights = [
                insight
                for query, query_result in zip(queries, query_results)
                for insight in session.container.insight_service.generate(query, query_result)
            ]
            insight_objects = session.container.insight_service.objects()
            conclusions = session.container.reasoning_service.generate(insight_objects)
            session.analysis_result = {
                "import": imported,
                "transaction_count": imported["accepted_rows"],
                "query": {
                    "summary": dict(query_results[0].summary), "query_id": queries[0].id,
                    "warnings": query_results[0].warnings,
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
