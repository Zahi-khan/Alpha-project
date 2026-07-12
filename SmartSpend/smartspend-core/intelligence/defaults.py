"""Default composition of Financial Intelligence capabilities."""

from analytics.anomalies.anomaly_analysis import AnomalyAnalysis
from analytics.cashflow.cashflow_analysis import CashFlowAnalysis
from analytics.forecast_analysis import ForecastAnalysis
from analytics.savings_analysis import SavingsAnalysis
from analytics.spending.spending_analysis import SpendingAnalysis
from analytics.trends.trend_analysis import TrendAnalysis
from intelligence.core.registry import IntelligenceRegistry
from intelligence.engines._adapter import AnalysisCapabilityAdapter


def build_default_intelligence_registry() -> IntelligenceRegistry:
    registry = IntelligenceRegistry()
    for analysis in (CashFlowAnalysis(), SavingsAnalysis(), SpendingAnalysis(), TrendAnalysis(), ForecastAnalysis(), AnomalyAnalysis()):
        registry.register(AnalysisCapabilityAdapter(analysis))
    return registry
