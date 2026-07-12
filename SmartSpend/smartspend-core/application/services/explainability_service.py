"""Stable application-facing traces that hide explainability graph internals."""

from application.errors.not_found_error import NotFoundError
from intelligence.core.insight import FinancialInsight
from memory.enriched_transaction import EnrichedTransaction
from query.query import FinancialQuery
from reasoning.explainability_graph import ExplainabilityGraph


class ExplainabilityService:
    def __init__(self, graph: ExplainabilityGraph): self._graph = graph

    def trace(self, root_id: str) -> dict:
        node_ids = self._graph.trace(root_id)
        if not node_ids: raise NotFoundError("Explainability trace not found.")
        root = self._graph.node(root_id)
        transaction_nodes = tuple(node_id for node_id in node_ids if node_id.startswith("transaction:"))
        steps = [self._describe(node_id) for node_id in node_ids if not node_id.startswith("transaction:")]
        if transaction_nodes:
            steps.extend(self._describe(node_id) for node_id in transaction_nodes[:3])
            remaining = len(transaction_nodes) - 3
            if remaining > 0:
                steps.append(f"{remaining} additional related transactions were included in the verified query.")
        return {
            "root_id": root_id,
            "nodes": node_ids,
            "transaction_ids": tuple(node.split(":", 1)[1] for node in node_ids if node.startswith("transaction:")),
            "title": root.title if isinstance(root, FinancialInsight) else "Why SmartSpend produced this result",
            "summary": root.summary if isinstance(root, FinancialInsight) else "This result is based on verified financial evidence.",
            "steps": tuple(steps),
            "warnings": (),
        }

    def _describe(self, node_id: str) -> str:
        node = self._graph.node(node_id)
        if isinstance(node, FinancialInsight):
            return node.summary
        if isinstance(node, FinancialQuery):
            return "SmartSpend ran a verified financial query over the transactions in this private session."
        if isinstance(node, EnrichedTransaction):
            merchant = node.merchant.canonical_name if node.merchant else node.transaction.description
            category = node.category.name if node.category else "Uncategorized"
            return f"Included transaction: {merchant} in {category}."
        return "A linked processing result supports this explanation."
