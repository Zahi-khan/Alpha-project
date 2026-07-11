"""Idempotent cleanup facade for request and startup expiry checks."""

from application.sessions.session_manager import SessionManager


class CleanupService:
    def __init__(self, sessions: SessionManager): self._sessions = sessions
    def cleanup_session(self, session_id: str) -> None: self._sessions.cleanup(session_id)
    def cleanup_expired(self) -> None: self._sessions.cleanup_expired()
