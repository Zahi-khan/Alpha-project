"""Uniform contract for financial-intelligence capabilities."""

from __future__ import annotations

from typing import Protocol

from intelligence.core.intelligence_context import IntelligenceContext


class IntelligenceCapability(Protocol):
    name: str
    def evaluate(self, context: IntelligenceContext) -> None:
        """Add explainable insights to a context without changing its query result."""
