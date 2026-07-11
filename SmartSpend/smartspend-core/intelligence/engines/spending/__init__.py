"""Spending intelligence capability."""

from analytics.spending.spending_analysis import SpendingAnalysis
from intelligence.engines._adapter import AnalysisCapabilityAdapter

SpendingEngine = AnalysisCapabilityAdapter

__all__ = ["SpendingAnalysis", "SpendingEngine"]
