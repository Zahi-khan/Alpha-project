"""Decimal-safe currency display with Indian grouping support."""

from decimal import Decimal


def format_currency(value: Decimal, currency: str = "INR", compact: bool = False) -> str:
    sign = "-" if value < 0 else ""
    amount = abs(value)
    if compact and currency == "INR" and amount >= Decimal("100000"):
        return f"{sign}₹{(amount / Decimal('100000')):.1f}L"
    if currency == "INR":
        text = f"{amount:,.2f}".rstrip("0").rstrip(".")
        whole, *fraction = text.split(".")
        if len(whole) > 3:
            tail, head = whole[-3:], whole[:-3]
            groups = []
            while head:
                groups.append(head[-2:]); head = head[:-2]
            whole = ",".join(reversed(groups)) + "," + tail
        return f"{sign}₹{whole}{'.' + fraction[0] if fraction else ''}"
    return f"{sign}{currency} {amount:,.2f}"
