from app.core.exceptions.domain.base import DomainValidationException


class InvalidTimezone(DomainValidationException):
    def __init__(
        self,
        timezone: str,
        message: str = "Invalid timezone value",
    ) -> None:
        super().__init__(
            message=message,
            details={"timezone": timezone},
        )
