"""Compatibility import for the shared baseline subsystem."""

from intelligence.baselines.baseline_engine import BaselineEngine

BaselineService = BaselineEngine

__all__ = ["BaselineService"]
