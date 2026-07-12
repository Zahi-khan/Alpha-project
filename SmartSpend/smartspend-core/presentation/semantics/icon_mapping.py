"""Stable icon keys, never frontend-specific icon components."""


def icon_for_insight_type(insight_type: str) -> str:
    return {"trend": "trend_up", "spending": "wallet", "savings": "savings", "recurring": "repeat", "cash_flow": "cashflow", "forecast": "forecast", "financial_health": "savings", "anomaly": "alert", "risk": "shield"}.get(insight_type, "insight")
