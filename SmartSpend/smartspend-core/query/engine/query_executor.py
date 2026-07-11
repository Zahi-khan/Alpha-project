"""Apply filters, grouping, metrics, sorting, and limits to a query plan."""

from __future__ import annotations

from collections import defaultdict
from types import MappingProxyType
from typing import Any

from query.metrics.count import CountMetric
from query.query import FinancialQuery
from query.query_result import QueryResult, QueryRow


class QueryExecutor:
    def execute(self, query: FinancialQuery, plan, execution_time_ms: float) -> QueryResult:
        items = [item for item in plan.seed if all(filter_.matches(item) for filter_ in query.filters)]
        metrics = query.metrics or (CountMetric(),)
        groups: dict[str | None, list[Any]] = defaultdict(list)
        if query.group_by is None:
            groups[None] = items
        else:
            for item in items:
                groups[query.group_by.key_for(item)].append(item)

        rows = tuple(
            QueryRow(group, MappingProxyType({metric.name: metric.calculate(group_items) for metric in metrics}))
            for group, group_items in groups.items()
        )
        if query.sort_by is not None:
            rows = tuple(sorted(rows, key=lambda row: row.values.get(query.sort_by), reverse=query.descending))
        if query.limit is not None:
            rows = rows[:query.limit]
        summary = {metric.name: metric.calculate(items) for metric in metrics}
        warnings = () if query.metrics else ("No metric requested; defaulted to count.",)
        return QueryResult(
            rows=rows,
            summary=MappingProxyType(summary),
            execution_time_ms=execution_time_ms,
            metadata=MappingProxyType({
                "index_used": plan.index_used,
                "scanned_transactions": len(plan.seed),
                "matched_transactions": len(items),
                "matched_transaction_ids": tuple(
                    item.transaction.id for item in items if item.transaction.id is not None
                ),
            }),
            warnings=warnings,
            query_id=query.id,
        )
