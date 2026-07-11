"""Convert technical provenance into a readable explanation view."""

from presentation.models.views import ExplanationView


class ExplainabilityPresenter:
    def present(self, trace: dict, context):
        transactions = tuple(trace.get("transaction_ids", ()))
        steps = tuple(f"Verified evidence step: {node}" for node in trace.get("nodes", ()))
        return ExplanationView("Why SmartSpend produced this result", "This result is based on linked financial evidence and verified processing steps.", steps, transactions)
