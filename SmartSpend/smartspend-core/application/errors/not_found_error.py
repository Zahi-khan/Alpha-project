"""Requested application entity was not found."""

from application.errors.application_error import ApplicationError


class NotFoundError(ApplicationError):
    status_code = 404
    code = "not_found"
