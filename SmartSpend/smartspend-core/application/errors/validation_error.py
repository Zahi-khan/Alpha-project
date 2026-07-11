"""Input validation failure."""

from application.errors.application_error import ApplicationError


class ValidationError(ApplicationError):
    code = "validation_error"
