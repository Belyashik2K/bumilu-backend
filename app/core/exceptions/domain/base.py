from collections.abc import Mapping
from typing import (
    Any,
)

from app.core.exceptions.base import BaseProjectException
from app.core.exceptions.domain.error_code import DomainErrorCodeEnum


class BaseDomainException(BaseProjectException):
    def __init__(
        self,
        message: str,
        code: DomainErrorCodeEnum,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.details = details
        super().__init__(message)

    def __str__(self) -> str:
        exc_str = f"{self.__class__.__name__}({self.code}): {self.message}"
        if self.details:
            exc_str += f", has details: {self.details}" if self.details else ""
        return exc_str


class DomainValidationException(BaseDomainException):
    def __init__(self, message: str, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(
            message=message, code=DomainErrorCodeEnum.VALIDATION, details=details
        )


class DomainInvariantViolationException(BaseDomainException):
    def __init__(self, message: str, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(
            message=message,
            code=DomainErrorCodeEnum.INVARIANT_VIOLATION,
            details=details,
        )


class DomainConflictException(BaseDomainException):
    def __init__(self, message: str, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(
            message=message, code=DomainErrorCodeEnum.CONFLICT, details=details
        )
