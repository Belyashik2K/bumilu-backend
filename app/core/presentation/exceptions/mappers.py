from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
)

from app.core.shared.exceptions.application import (
    BaseApplicationException,
)
from app.core.shared.exceptions.application.error_code import ApplicationErrorCodeEnum
from app.core.shared.exceptions.domain.base import BaseDomainException
from app.core.shared.exceptions.domain.error_code import DomainErrorCodeEnum


def map_domain_exception_to_http(exc: BaseDomainException) -> tuple[int, str]:
    code = exc.code

    exception_map = {
        DomainErrorCodeEnum.VALIDATION: (HTTP_400_BAD_REQUEST, exc.message),
        DomainErrorCodeEnum.CONFLICT: (HTTP_409_CONFLICT, exc.message),
        DomainErrorCodeEnum.INVARIANT_VIOLATION: (HTTP_409_CONFLICT, exc.message),
    }
    default_response = (HTTP_400_BAD_REQUEST, exc.message)

    return exception_map.get(code, default_response)


def map_app_exception_to_http(exc: BaseApplicationException) -> tuple[int, str]:
    code = exc.code

    exception_map = {
        ApplicationErrorCodeEnum.UNAUTHORIZED: (HTTP_401_UNAUTHORIZED, exc.message),
        ApplicationErrorCodeEnum.FORBIDDEN: (HTTP_403_FORBIDDEN, exc.message),
        ApplicationErrorCodeEnum.NOT_FOUND: (HTTP_404_NOT_FOUND, exc.message),
        ApplicationErrorCodeEnum.CONFLICT: (HTTP_409_CONFLICT, exc.message),
        ApplicationErrorCodeEnum.RATE_LIMIT_EXCEEDED: (
            HTTP_429_TOO_MANY_REQUESTS,
            exc.message,
        ),
        ApplicationErrorCodeEnum.SERVICE_UNAVAILABLE: (
            HTTP_503_SERVICE_UNAVAILABLE,
            exc.message,
        ),
    }
    default_response = (HTTP_500_INTERNAL_SERVER_ERROR, exc.message)

    return exception_map.get(code, default_response)
