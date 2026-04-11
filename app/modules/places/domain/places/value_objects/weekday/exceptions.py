from app.core.exceptions.domain.base import DomainValidationException


class InvalidWeekday(DomainValidationException):
    def __init__(self, weekday: int) -> None:
        super().__init__(message=f"Invalid weekday value: '{weekday}'")
