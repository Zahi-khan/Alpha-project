"""Adapts existing analysis modules to the Financial Intelligence contract."""

from intelligence.core.intelligence_context import IntelligenceContext


class AnalysisCapabilityAdapter:
    def __init__(self, analysis):
        self._analysis = analysis
        self.name = analysis.name

    def evaluate(self, context: IntelligenceContext) -> None:
        self._analysis.analyze(context)
