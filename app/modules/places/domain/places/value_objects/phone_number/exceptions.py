from app.core.exceptions.domain.base import DomainValidationException


class InvalidPlacePhoneNumber(DomainValidationException):
    def __init__(self, message: str = "Invalid phone number format.") -> None:
        super().__init__(message)
