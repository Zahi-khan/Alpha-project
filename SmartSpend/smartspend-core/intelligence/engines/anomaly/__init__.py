"""Anomaly intelligence capability."""

from analytics.anomalies.anomaly_analysis import AnomalyAnalysis
from intelligence.engines._adapter import AnalysisCapabilityAdapter

AnomalyEngine = AnalysisCapabilityAdapter

__all__ = ["AnomalyAnalysis", "AnomalyEngine"]
