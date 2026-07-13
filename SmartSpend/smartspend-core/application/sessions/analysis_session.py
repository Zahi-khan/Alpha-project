"""One anonymous, isolated analysis job with no permanent user identity."""

from __future__ import annotations

from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from application.sessions.session_status import SessionStatus
from models._dataclasses import slotted_dataclass

if TYPE_CHECKING:
    from application.container import ApplicationContainer


@slotted_dataclass
class AnalysisSession:
    session_id: str
    created_at: datetime
    expires_at: datetime
    root_path: Path
    container: ApplicationContainer
    status: SessionStatus = SessionStatus.CREATED
    detected_bank: str | None = None
    detected_account_mask: str | None = None
    analysis_result: dict[str, Any] = field(default_factory=dict)
    report_path: Path | None = None
    warnings: list[str] = field(default_factory=list)
    error: str | None = None
    pdf_password_failures: int = 0
