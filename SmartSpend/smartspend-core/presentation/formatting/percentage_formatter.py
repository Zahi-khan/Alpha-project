"""Human-safe percentage formatting."""


def format_percentage(value, precision: int = 1) -> str:
    return f"{float(value):.{precision}f}%"
