from app.core.exceptions.domain.base import DomainConflictException


class DeviceAlreadyAttachedToDifferentGuestUser(DomainConflictException):
    def __init__(self) -> None:
        super().__init__(message="Device already attached to a different guest user.")
