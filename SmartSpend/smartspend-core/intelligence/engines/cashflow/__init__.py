"""Cash-flow intelligence capability."""

from analytics.cashflow.cashflow_analysis import CashFlowAnalysis
from intelligence.engines._adapter import AnalysisCapabilityAdapter

CashFlowEngine = AnalysisCapabilityAdapter

__all__ = ["CashFlowAnalysis", "CashFlowEngine"]
