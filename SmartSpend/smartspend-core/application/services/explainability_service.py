"""Stable application-facing traces that hide explainability graph internals."""

from application.errors.not_found_error import NotFoundError
from reasoning.explainability_graph import ExplainabilityGraph


class ExplainabilityService:
    def __init__(self, graph: ExplainabilityGraph): self._graph = graph

    def trace(self, root_id: str) -> dict:
        node_ids = self._graph.trace(root_id)
        if not node_ids: raise NotFoundError("Explainability trace not found.")
        return {
            "root_id": root_id,
            "nodes": node_ids,
            "transaction_ids": tuple(node.split(":", 1)[1] for node in node_ids if node.startswith("transaction:")),
            "warnings": (),
        }
