"""Compatibility import for the canonical payment-detection stage."""

from intelligence.stages.payment_detection_stage import PaymentDetectionStage

PaymentDetector = PaymentDetectionStage

__all__ = ["PaymentDetector"]
