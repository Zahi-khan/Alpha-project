"""Backward-traceable references from recommendations to supporting insights."""

from __future__ import annotations

from collections import defaultdict

from intelligence.core.insight import FinancialInsight
from memory.enriched_transaction import EnrichedTransaction
from models.financial_conclusion import FinancialConclusion
from models.recommendation import Recommendation
from query.query import FinancialQuery
from query.query_result import QueryResult


class ExplainabilityGraph:
    """A directed graph where each node points to the evidence it depends on."""

    def __init__(self):
        self._parents: dict[str, set[str]] = defaultdict(set)
        self._nodes: dict[str, object] = {}

    def add_insight(self, insight: FinancialInsight) -> None:
        self._nodes[insight.id] = insight
        query = insight.supporting_query
        if isinstance(query, FinancialQuery):
            self._parents[insight.id].add(query.id)

    def add_query(self, query: FinancialQuery, result: QueryResult) -> None:
        """Link a query to the enriched transactions selected for its result."""
        self._nodes[query.id] = query
        self._nodes[f"query_result:{query.id}"] = result
        self._parents[query.id].update(
            f"transaction:{transaction_id}"
            for transaction_id in result.metadata.get("matched_transaction_ids", ())
        )

    def add_enriched_transaction(self, transaction: EnrichedTransaction) -> None:
        transaction_id = transaction.transaction.id
        if transaction_id is not None:
            self._nodes[f"transaction:{transaction_id}"] = transaction

    def add_conclusion(self, conclusion: FinancialConclusion) -> None:
        self._nodes[conclusion.id] = conclusion
        self._parents[conclusion.id].update(conclusion.supporting_insight_ids)

    def add_recommendation(self, recommendation: Recommendation) -> None:
        self._nodes[recommendation.id] = recommendation
        self._parents[recommendation.id].update(recommendation.supporting_conclusion_ids)

    def trace(self, node_id: str) -> tuple[str, ...]:
        """Return the node and every upstream dependency in deterministic order."""
        if node_id not in self._nodes:
            return ()
        visited: set[str] = set()
        ordered: list[str] = []

        def walk(current: str) -> None:
            if current in visited:
                return
            visited.add(current)
            ordered.append(current)
            for parent in sorted(self._parents[current]):
                walk(parent)

        walk(node_id)
        return tuple(ordered)

    def clear(self) -> None:
        """Discard all session-owned provenance nodes and edges."""
        self._parents.clear()
        self._nodes.clear()
