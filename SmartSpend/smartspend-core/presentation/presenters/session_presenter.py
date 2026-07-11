"""Translate technical session lifecycle status into calm human-facing wording."""

from presentation.models.views import SessionView


class SessionPresenter:
    _LABELS = {
        "created": ("Ready for upload", "waiting_for_statement"),
        "processing": ("Understanding your statement", "merchant_resolution"),
        "analyzed": ("Analysis ready", "financial_memory"),
        "report_ready": ("Your private report is ready", "report_generation"),
        "finalizing": ("Download window ending soon", "cleanup"),
        "failed": ("Analysis could not be completed", "error"),
    }
    def present(self, session, context):
        label, stage = self._LABELS.get(session.status.value, (session.status.value.title(), "unknown"))
        return SessionView(session.session_id, session.status.value, label, stage, session.expires_at, session.report_path is not None, session.report_path is not None and session.status.value != "expired", "Your uploaded statement and analysis are temporary and automatically deleted when this session expires.")
