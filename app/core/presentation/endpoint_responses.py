from typing import Any

from starlette import status

from app.core.presentation.exceptions.response import (
    ErrorResponseSchema,
    ValidationErrorResponseSchema,
)

mapped_code_to_exception = {
    status.HTTP_200_OK: (None, "Successful request"),
    status.HTTP_201_CREATED: (None, "Resource created successfully"),
    status.HTTP_204_NO_CONTENT: (
        None,
        "Server successfully processed the request, but is not returning any content",
    ),
    status.HTTP_400_BAD_REQUEST: (ErrorResponseSchema, "Bad request error occurred"),
    status.HTTP_401_UNAUTHORIZED: (ErrorResponseSchema, "Unauthorized access"),
    status.HTTP_403_FORBIDDEN: (ErrorResponseSchema, "Forbidden access"),
    status.HTTP_404_NOT_FOUND: (ErrorResponseSchema, "Resource not found"),
    status.HTTP_409_CONFLICT: (ErrorResponseSchema, "Resource conflict"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: (
        ValidationErrorResponseSchema,
        "Validation error occurred",
    ),
    status.HTTP_429_TOO_MANY_REQUESTS: (ErrorResponseSchema, "Too many requests"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: (
        ErrorResponseSchema,
        "Internal server error occurred",
    ),
    status.HTTP_501_NOT_IMPLEMENTED: (
        ErrorResponseSchema,
        "I'll work on it, promise!",
    ),
    status.HTTP_503_SERVICE_UNAVAILABLE: (
        ErrorResponseSchema,
        "Service is currently unavailable",
    ),
}

DEFAULT = [
    status.HTTP_400_BAD_REQUEST,
    status.HTTP_401_UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN,
    status.HTTP_422_UNPROCESSABLE_ENTITY,
    status.HTTP_429_TOO_MANY_REQUESTS,
    status.HTTP_500_INTERNAL_SERVER_ERROR,
    status.HTTP_503_SERVICE_UNAVAILABLE,
]


def generate_response_model_for_code(status_code: int) -> dict[str, Any]:
    default = {"description": mapped_code_to_exception[status_code][1]}
    if mapped_code_to_exception[status_code][0] is not None:
        default["model"] = mapped_code_to_exception[status_code][0]  # type: ignore
    return default


def generate_responses_for_endpoint(
    *status_codes: int, include_defaults: bool = True
) -> dict[int | str, dict[str, Any]]:
    responses: dict[int | str, dict[str, Any]] = {}

    statuses = DEFAULT if include_defaults else []

    for status_code in statuses + list(status_codes):
        responses[status_code] = generate_response_model_for_code(status_code)
    return responses
