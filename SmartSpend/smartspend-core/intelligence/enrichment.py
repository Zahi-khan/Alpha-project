"""Factories for assembling SmartSpend's standard intelligence pipeline."""

from intelligence.matchers.alias_matcher import AliasMatcher
from intelligence.pipeline.pipeline import EnrichmentPipeline
from intelligence.pipeline.validator import ValidationStage
from intelligence.stages.category_resolution_stage import CategoryResolutionStage
from intelligence.stages.confidence_stage import ConfidenceStage
from intelligence.stages.industry_resolution_stage import IndustryResolutionStage
from intelligence.stages.merchant_resolution_stage import MerchantResolutionStage
from intelligence.stages.normalization_stage import NormalizationStage
from intelligence.stages.payment_detection_stage import PaymentDetectionStage
from intelligence.stages.recurring_detection_stage import RecurringDetectionStage
from intelligence.stages.transaction_type_stage import TransactionTypeStage
from knowledge.knowledge_base import KnowledgeBase


def build_enrichment_pipeline(knowledge: KnowledgeBase) -> EnrichmentPipeline:
    """Create the default ordered, explainable intelligence pipeline."""
    return EnrichmentPipeline(
        [
            NormalizationStage(),
            MerchantResolutionStage(AliasMatcher(knowledge.find_merchant)),
            PaymentDetectionStage(),
            TransactionTypeStage(),
            CategoryResolutionStage(),
            IndustryResolutionStage(),
            RecurringDetectionStage(),
            ConfidenceStage(),
            ValidationStage(),
        ]
    )
