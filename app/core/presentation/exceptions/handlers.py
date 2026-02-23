from collections.abc import Mapping
from typing import (
    Any,
)

from fastapi import FastAPI
from starlette.requests import Request
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.presentation.exceptions.mappers import (
    map_app_exception_to_http,
    map_domain_exception_to_http,
)
from app.core.presentation.exceptions.response import ErrorResponseSchema
from app.core.shared.exceptions import (
    BaseApplicationException,
    BaseDomainException,
)


def _safe_details(details: Mapping[str, Any] | None = None) -> Mapping[str, Any] | None:
    if details is None:
        return None
    return {k: str(v) for k, v in details.items()}


def _prepare_response(
    status_code: int,
    message: str,
    default_response_class: type,
    details: Mapping[str, Any] | None = None,
) -> dict:
    payload = ErrorResponseSchema(
        error_message=message,
        details=_safe_details(details),
    ).model_dump(exclude_none=True)
    return default_response_class(status_code=status_code, content=payload)


def set_exception_handlers(app: FastAPI, default_response_class: type):
    @app.exception_handler(BaseDomainException)
    async def domain_exception_handler(request: Request, exc: BaseDomainException):
        status_code, public_message = map_domain_exception_to_http(exc)
        return _prepare_response(
            status_code=status_code,
            message=public_message,
            default_response_class=default_response_class,
            details=exc.details,
        )

    @app.exception_handler(BaseApplicationException)
    async def app_exception_handler(request: Request, exc: BaseApplicationException):
        status_code, public_message = map_app_exception_to_http(exc)
        return _prepare_response(
            status_code=status_code,
            message=public_message,
            default_response_class=default_response_class,
            details=exc.details,
        )

    @app.exception_handler(Exception)
    async def fallback_handler(request: Request, exc: Exception):
        return _prepare_response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            message="An unexpected error occurred. Please try again later.",
            default_response_class=default_response_class,
            details=None,
        )
