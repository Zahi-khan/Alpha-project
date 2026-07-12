"""Default analytics registry composition."""

from analytics.anomalies.anomaly_analysis import AnomalyAnalysis
from analytics.cashflow.cashflow_analysis import CashFlowAnalysis
from analytics.forecast_analysis import ForecastAnalysis
from analytics.savings_analysis import SavingsAnalysis
from analytics.core.registry import AnalyticsRegistry
from analytics.spending.spending_analysis import SpendingAnalysis
from analytics.trends.trend_analysis import TrendAnalysis


def build_default_registry() -> AnalyticsRegistry:
    registry = AnalyticsRegistry()
    for module in (CashFlowAnalysis(), SavingsAnalysis(), SpendingAnalysis(), TrendAnalysis(), ForecastAnalysis(), AnomalyAnalysis()):
        registry.register(module)
    return registry
