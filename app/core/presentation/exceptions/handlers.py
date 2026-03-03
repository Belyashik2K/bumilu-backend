import logging
from collections.abc import Mapping
from typing import (
    Any,
)

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import (
    JSONResponse,
)
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

logger = logging.getLogger(__name__)


def _safe_details(details: Mapping[str, Any] | None) -> Mapping[str, Any] | None:
    return details or {}


def _pydantic_422_details(exc: RequestValidationError) -> Mapping[str, Any]:
    errors = []
    for e in exc.errors():
        loc = e.get("loc", ())
        field = (
            ".".join(str(x) for x in loc[1:])
            if len(loc) > 1
            else ".".join(str(x) for x in loc)
        )
        errors.append(
            {
                "field": field or None,
                "location": loc[0] if loc else None,
                "message": e.get("msg"),
                "type": e.get("type"),
            }
        )
    return {"validation_errors": errors}


def _prepare_response(
    status_code: int,
    message: str,
    details: Mapping[str, Any] | None = None,
) -> JSONResponse:
    payload = ErrorResponseSchema(
        error_message=message,
        details=_safe_details(details),
    ).model_dump(exclude_none=True)
    return JSONResponse(status_code=status_code, content=payload)


def set_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return _prepare_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Validation error",
            details=_pydantic_422_details(exc),
        )

    @app.exception_handler(BaseDomainException)
    async def domain_exception_handler(
        request: Request, exc: BaseDomainException
    ) -> JSONResponse:
        status_code, public_message = map_domain_exception_to_http(exc)
        return _prepare_response(
            status_code=status_code,
            message=public_message,
            details=exc.details,
        )

    @app.exception_handler(BaseApplicationException)
    async def app_exception_handler(
        request: Request, exc: BaseApplicationException
    ) -> JSONResponse:
        logger.error("An unexpected error occurred", exc_info=exc)
        status_code, public_message = map_app_exception_to_http(exc)
        return _prepare_response(
            status_code=status_code,
            message=public_message,
            details=exc.details,
        )

    @app.exception_handler(NotImplementedError)
    async def not_implemented_exception_handler(
        request: Request, exc: NotImplementedError
    ) -> JSONResponse:
        return _prepare_response(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            message="This functionality is not implemented yet.",
            details={"error": str(exc)},
        )

    @app.exception_handler(Exception)
    async def fallback_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error("An unexpected error occurred", exc_info=exc)
        return _prepare_response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            message="An unexpected error occurred. Please try again later.",
            details=None,
        )
