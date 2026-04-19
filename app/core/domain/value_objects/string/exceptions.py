from app.core.exceptions.domain.base import DomainValidationException


class InvalidString(DomainValidationException):
    def __init__(self, message: str | None = None) -> None:
        message = message or "Invalid string value"
        super().__init__(message)
