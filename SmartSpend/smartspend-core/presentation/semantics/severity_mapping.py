"""Map verified semantic severity to UI-neutral tones."""


def tone_for_severity(severity: str) -> str:
    return {"critical": "critical", "high": "critical", "medium": "warning", "low": "informational", "informational": "neutral"}.get(severity, "neutral")
