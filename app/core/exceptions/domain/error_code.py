from enum import (
    StrEnum,
)


class DomainErrorCodeEnum(StrEnum):
    INVARIANT_VIOLATION = "invariant_violation"
    VALIDATION = "validation"
    CONFLICT = "conflict"
