"""Uniform deterministic presenter contract."""

from __future__ import annotations

from typing import Protocol

from presentation.core.presentation_context import PresentationContext


class Presenter(Protocol):
    def present(self, source, context: PresentationContext):
        """Convert a verified source object into an immutable view model."""
