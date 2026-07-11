"""Lifecycle states for privacy-first analysis sessions."""

from enum import Enum


class SessionStatus(str, Enum):
    CREATED = "created"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    ANALYZED = "analyzed"
    REPORT_READY = "report_ready"
    FINALIZING = "finalizing"
    DELETED = "deleted"
    FAILED = "failed"
    EXPIRED = "expired"
