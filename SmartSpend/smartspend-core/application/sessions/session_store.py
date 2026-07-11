"""In-memory store for ephemeral sessions; replaceable by a TTL-backed store."""

from __future__ import annotations

from application.sessions.analysis_session import AnalysisSession


class InMemorySessionStore:
    def __init__(self): self._sessions: dict[str, AnalysisSession] = {}
    def add(self, session: AnalysisSession) -> None: self._sessions[session.session_id] = session
    def get(self, session_id: str) -> AnalysisSession | None: return self._sessions.get(session_id)
    def remove(self, session_id: str) -> AnalysisSession | None: return self._sessions.pop(session_id, None)
    def all(self) -> tuple[AnalysisSession, ...]: return tuple(self._sessions.values())
