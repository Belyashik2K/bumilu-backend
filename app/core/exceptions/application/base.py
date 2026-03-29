from collections.abc import Mapping
from typing import (
    Any,
)

from app.core.exceptions.application.error_code import ApplicationErrorCodeEnum
from app.core.exceptions.base import BaseProjectException


class BaseApplicationException(BaseProjectException):
    def __init__(
        self,
        message: str,
        code: ApplicationErrorCodeEnum,
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


class ApplicationNotFoundException(BaseApplicationException):
    def __init__(self, message: str, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(
            message=message, code=ApplicationErrorCodeEnum.NOT_FOUND, details=details
        )


class ApplicationConflictException(BaseApplicationException):
    def __init__(self, message: str, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(
            message=message, code=ApplicationErrorCodeEnum.CONFLICT, details=details
        )


class ApplicationUnauthorizedException(BaseApplicationException):
    def __init__(self, message: str, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(
            message=message,
            code=ApplicationErrorCodeEnum.UNAUTHORIZED,
            details=details,
        )


class ApplicationForbiddenException(BaseApplicationException):
    def __init__(self, message: str, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(
            message=message, code=ApplicationErrorCodeEnum.FORBIDDEN, details=details
        )


class ApplicationRateLimitExceededException(BaseApplicationException):
    def __init__(self, message: str, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(
            message=message,
            code=ApplicationErrorCodeEnum.RATE_LIMIT_EXCEEDED,
            details=details,
        )


class ApplicationServiceUnavailableException(BaseApplicationException):
    def __init__(
        self,
        message: str = "Service is currently unavailable. Please try again later.",
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code=ApplicationErrorCodeEnum.SERVICE_UNAVAILABLE,
            details=details,
        )


class ApplicationUnexpectedException(BaseApplicationException):
    def __init__(
        self,
        message: str = "An unexpected error occurred. Please try again later.",
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message, code=ApplicationErrorCodeEnum.UNEXPECTED, details=details
        )
