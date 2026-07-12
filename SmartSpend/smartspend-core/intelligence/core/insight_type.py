"""Stable classifications for Financial Intelligence insights."""

from enum import Enum


class InsightType(str, Enum):
    CASH_FLOW = "cash_flow"
    SPENDING = "spending"
    TREND = "trend"
    ANOMALY = "anomaly"
    BEHAVIOR = "behavior"
    RECURRING = "recurring"
    BUDGET = "budget"
    FINANCIAL_HEALTH = "financial_health"
    RISK = "risk"
    FORECAST = "forecast"
    SAVINGS = "savings"
