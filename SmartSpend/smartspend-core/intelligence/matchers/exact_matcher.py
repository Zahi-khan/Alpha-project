"""Exact canonical-name or identifier lookup."""

from __future__ import annotations

from collections.abc import Callable

from models.merchant import Merchant


class ExactMatcher:
    def __init__(self, find_merchant: Callable[[str], Merchant | None]):
        self._find_merchant = find_merchant

    def match(self, query: str) -> Merchant | None:
        return self._find_merchant(query)
