from enum import StrEnum


class ApplicationErrorCodeEnum(StrEnum):
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    UNEXPECTED = "unexpected"
    SERVICE_UNAVAILABLE = "service_unavailable"
    TOO_MANY_REQUESTS = "too_many_requests"
