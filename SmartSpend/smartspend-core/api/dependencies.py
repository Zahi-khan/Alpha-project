"""FastAPI dependency access to the single application composition root."""

from functools import lru_cache

from application.container import ApplicationContainer
from application.sessions.session_manager import SessionManager


@lru_cache(maxsize=1)
def get_container() -> ApplicationContainer:
    return ApplicationContainer()


@lru_cache(maxsize=1)
def get_session_manager() -> SessionManager:
    return SessionManager()
