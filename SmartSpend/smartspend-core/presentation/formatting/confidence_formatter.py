"""Configuration-friendly confidence labels."""


def format_confidence(value: float) -> str:
    if value >= 0.90: return "High confidence"
    if value >= 0.70: return "Moderate confidence"
    if value >= 0.50: return "Limited confidence"
    return "Low confidence"
