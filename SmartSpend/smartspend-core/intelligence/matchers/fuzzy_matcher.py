"""Extension point for typo-tolerant merchant matching."""

from __future__ import annotations

from models.merchant import Merchant


class FuzzyMatcher:
    def match(self, query: str) -> Merchant | None:
        return None
