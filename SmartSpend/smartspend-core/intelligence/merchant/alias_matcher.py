"""Exact alias matching backed by a merchant lookup function."""

from __future__ import annotations

from collections.abc import Callable

from models.merchant import Merchant


class AliasMatcher:
    """Finds a canonical merchant from an ID, name, or known alias."""

    def __init__(self, find_merchant: Callable[[str], Merchant | None]):
        self._find_merchant = find_merchant

    def match(self, query: str) -> Merchant | None:
        return self._find_merchant(query)
