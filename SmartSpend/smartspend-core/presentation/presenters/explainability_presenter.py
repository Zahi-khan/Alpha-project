"""Convert technical provenance into a readable explanation view."""

from presentation.models.views import ExplanationView


class ExplainabilityPresenter:
    def present(self, trace: dict, context):
        transactions = tuple(trace.get("transaction_ids", ()))
        steps = tuple(trace.get("steps", ()))
        return ExplanationView(trace.get("title", "Why SmartSpend produced this result"), trace.get("summary", "This result is based on linked financial evidence and verified processing steps."), steps, transactions)
