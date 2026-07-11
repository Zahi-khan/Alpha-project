"""Extension point for future embedding- or LLM-based matching."""

from __future__ import annotations

from models.merchant import Merchant


class SemanticMatcher:
    def match(self, query: str) -> Merchant | None:
        return None
