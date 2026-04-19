from datetime import datetime

from app.core.exceptions.domain.base import (
    DomainInvariantViolationException,
    DomainValidationException,
)


class SessionExpirationMustBeInFuture(DomainValidationException):
    def __init__(self, expires_at: datetime) -> None:
        super().__init__(
            message="Expiration time must be in the future",
            details={"expires_at": expires_at.isoformat()},
        )


class CannotRotateInactiveSession(DomainInvariantViolationException):
    def __init__(self) -> None:
        super().__init__(message="Cannot rotate a revoked or expired session")
