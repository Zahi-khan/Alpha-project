"""Safe, structured failures for password-protected PDF statements."""

from application.errors.application_error import ApplicationError


class PdfPasswordRequiredError(ApplicationError):
    status_code = 422
    code = "pdf_password_required"


class InvalidPdfPasswordError(ApplicationError):
    status_code = 401
    code = "invalid_pdf_password"


class UnsupportedPdfEncryptionError(ApplicationError):
    status_code = 422
    code = "unsupported_pdf_encryption"


class PdfPasswordAttemptLimitError(ApplicationError):
    status_code = 429
    code = "pdf_password_attempt_limit"
