"""Shared workspace for independent financial-intelligence engines."""

from __future__ import annotations

from dataclasses import field, replace
from datetime import datetime
from typing import Any

from intelligence.core.insight import FinancialInsight
from models._dataclasses import slotted_dataclass
from query.query import FinancialQuery
from query.query_result import QueryResult


@slotted_dataclass
class IntelligenceContext:
    query_result: QueryResult
    supporting_query: FinancialQuery | None = None
    time_window: tuple[datetime | None, datetime | None] = (None, None)
    baselines: dict[str, Any] = field(default_factory=dict)
    previous_period: QueryResult | None = None
    configuration: dict[str, Any] = field(default_factory=dict)
    insights: list[FinancialInsight] = field(default_factory=list)
    statistics_cache: dict[str, Any] = field(default_factory=dict)

    def add_insight(self, insight: FinancialInsight) -> None:
        if insight.supporting_query is None and self.supporting_query is not None:
            insight = replace(insight, supporting_query=self.supporting_query)
        self.insights.append(insight)
