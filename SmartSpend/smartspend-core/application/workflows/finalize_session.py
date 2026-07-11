"""Mark a downloaded session for short-grace-period cleanup."""

from application.sessions.session_manager import SessionManager


class FinalizeSessionWorkflow:
    def __init__(self, sessions: SessionManager): self._sessions = sessions
    def finalize(self, session_id: str) -> None: self._sessions.mark_finalizing(session_id)
