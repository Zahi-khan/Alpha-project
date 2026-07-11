"""Creates, isolates, expires, and deletes anonymous analysis sessions."""

from __future__ import annotations

import secrets
import shutil
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from application.container import ApplicationContainer
from application.errors.not_found_error import NotFoundError
from application.sessions.analysis_session import AnalysisSession
from application.sessions.session_status import SessionStatus
from application.sessions.session_store import InMemorySessionStore


class SessionManager:
    def __init__(self, root: Path | None = None, lifetime_minutes: int = 60):
        self._root = root or Path(tempfile.gettempdir()) / "smartspend-sessions"
        self._root.mkdir(mode=0o700, parents=True, exist_ok=True)
        self._lifetime = timedelta(minutes=lifetime_minutes)
        self._store = InMemorySessionStore()

    def create(self) -> AnalysisSession:
        self.cleanup_expired()
        session_id = secrets.token_urlsafe(32)
        root = self._root / session_id
        for directory in (root / "upload", root / "working", root / "report"):
            directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        now = datetime.utcnow()
        session = AnalysisSession(session_id, now, now + self._lifetime, root, ApplicationContainer())
        self._store.add(session)
        return session

    def get(self, session_id: str) -> AnalysisSession:
        self.cleanup_expired()
        session = self._store.get(session_id)
        if session is None or session.status in (SessionStatus.DELETED, SessionStatus.EXPIRED):
            raise NotFoundError("Analysis session not found or expired.")
        return session

    def mark_finalizing(self, session_id: str, grace_minutes: int = 15) -> None:
        session = self.get(session_id)
        session.status = SessionStatus.FINALIZING
        session.expires_at = min(session.expires_at, datetime.utcnow() + timedelta(minutes=grace_minutes))

    def cleanup(self, session_id: str, expired: bool = False) -> None:
        session = self._store.remove(session_id)
        if session is None: return
        if session.root_path.parent == self._root:
            shutil.rmtree(session.root_path, ignore_errors=True)
        session.analysis_result.clear()
        session.warnings.clear()
        session.container.memory_store.clear()
        session.container.explainability_graph.clear()
        session.status = SessionStatus.EXPIRED if expired else SessionStatus.DELETED

    def cleanup_expired(self) -> None:
        now = datetime.utcnow()
        for session in self._store.all():
            if session.expires_at <= now:
                self.cleanup(session.session_id, expired=True)
