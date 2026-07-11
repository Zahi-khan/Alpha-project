"""Base safe error for caller-facing SmartSpend workflows."""


class ApplicationError(Exception):
    status_code = 400
    code = "application_error"
