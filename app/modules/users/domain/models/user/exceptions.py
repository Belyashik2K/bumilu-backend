from app.core.exceptions.domain.base import (
    DomainConflictException,
    DomainInvariantViolationException,
)


class VerifiedUserCannotBeGuest(DomainInvariantViolationException):
    def __init__(self) -> None:
        super().__init__(message="Verified user cannot be a guest.")


class UserEmailAlreadySet(DomainConflictException):
    def __init__(self) -> None:
        super().__init__(
            message="Email already set.",
        )


class CannotVerifyEmailWithoutEmail(DomainInvariantViolationException):
    def __init__(self) -> None:
        super().__init__(
            message="Cannot verify email without email address.",
        )
