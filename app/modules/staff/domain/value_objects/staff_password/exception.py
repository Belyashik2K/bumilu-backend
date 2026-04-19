from app.core.exceptions.domain.base import DomainValidationException


class InvalidStaffMemberPassword(DomainValidationException):
    def __init__(self, message: str) -> None:
        super().__init__(message=message)
