"""Extension point for future typo-tolerant merchant matching."""

from __future__ import annotations

from models.merchant import Merchant


class FuzzyMatcher:
    """A deliberate no-op until the repository exposes searchable candidates."""

    def match(self, query: str) -> Merchant | None:
        return None
