"""Fluent builder for FinancialQuery without query-execution logic."""

from __future__ import annotations

from typing import Any

from query.query import FinancialQuery


class FinancialQueryBuilder:
    def __init__(self):
        self._filters: list[Any] = []
        self._metrics: list[Any] = []
        self._group_by: Any | None = None
        self._sort_by: str | None = None
        self._descending = False
        self._limit: int | None = None
        self._output_format = "rows"
        self._metadata: dict[str, Any] = {}

    def where(self, filter_: Any) -> FinancialQueryBuilder:
        self._filters.append(filter_)
        return self

    def group(self, grouping: Any) -> FinancialQueryBuilder:
        self._group_by = grouping
        return self

    def metric(self, metric: Any) -> FinancialQueryBuilder:
        self._metrics.append(metric)
        return self

    def sort(self, value: str, descending: bool = False) -> FinancialQueryBuilder:
        self._sort_by = value
        self._descending = descending
        return self

    def take(self, limit: int) -> FinancialQueryBuilder:
        if limit < 1:
            raise ValueError("Query limit must be positive.")
        self._limit = limit
        return self

    def build(self) -> FinancialQuery:
        return FinancialQuery(
            filters=tuple(self._filters),
            group_by=self._group_by,
            metrics=tuple(self._metrics),
            sort_by=self._sort_by,
            descending=self._descending,
            limit=self._limit,
            output_format=self._output_format,
            metadata=dict(self._metadata),
        )
