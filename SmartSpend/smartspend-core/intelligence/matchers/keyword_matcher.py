"""Extension point for category fallback matching when merchant lookup fails."""

from models.category import Category


class KeywordMatcher:
    def match(self, query: str) -> Category | None:
        return None
