"""Stable names for evidence produced by pipeline stages."""

from enum import Enum


class EvidenceType(str, Enum):
    NORMALIZATION = "normalization"
    MERCHANT_MATCH = "merchant_match"
    PAYMENT_DETECTION = "payment_detection"
    TRANSACTION_TYPE = "transaction_type"
    CATEGORY_LINK = "category_link"
    INDUSTRY_LINK = "industry_link"
