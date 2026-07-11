"""Safe wrapper for processing failures that should not leak internals."""

from application.errors.application_error import ApplicationError


class ProcessingError(ApplicationError):
    status_code = 422
    code = "processing_error"
