from dataclasses import (
    dataclass,
    field,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceAddressReadModel:
    display: str
    taxi: str | None = field(default=None)
    taxi_comment: str | None = field(default=None)
