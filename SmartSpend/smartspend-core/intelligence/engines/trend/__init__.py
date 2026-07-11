"""Trend intelligence capability."""

from analytics.trends.trend_analysis import TrendAnalysis
from intelligence.engines._adapter import AnalysisCapabilityAdapter

TrendEngine = AnalysisCapabilityAdapter

__all__ = ["TrendAnalysis", "TrendEngine"]
