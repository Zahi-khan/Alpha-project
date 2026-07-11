"""Extension point for future embedding- or LLM-based merchant matching."""

from __future__ import annotations

from models.merchant import Merchant


class SemanticMatcher:
    """A deliberate no-op until a semantic model is configured."""

    def match(self, query: str) -> Merchant | None:
        return None
