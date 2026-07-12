"""Shared policy for separating essential costs from discretionary spending."""

from __future__ import annotations

ESSENTIAL_CATEGORY_TERMS = {
    "rent", "home", "housing", "loan", "emi", "insurance", "utility", "utilities",
    "groceries", "medicine", "health", "healthcare", "education", "investment", "tax",
}


def is_essential_category(category: str) -> bool:
    normalized = category.casefold()
    return any(term in normalized for term in ESSENTIAL_CATEGORY_TERMS)


def spending_type(category: str | None) -> str:
    if not category:
        return "unidentified"
    normalized = category.casefold()
    if "rent" in normalized or "home" in normalized or "housing" in normalized:
        return "rent"
    if any(term in normalized for term in ("food", "cafe", "dining", "restaurant")):
        return "food"
    if is_essential_category(category):
        return "essential"
    return "extra"
