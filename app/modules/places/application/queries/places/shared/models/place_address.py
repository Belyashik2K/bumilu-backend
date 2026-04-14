from dataclasses import (
    dataclass,
    field,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class BasePlaceAddressReadModel:
    taxi: str | None = field(default=None)
    taxi_comment: str | None = field(default=None)


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceAddressReadModel(BasePlaceAddressReadModel):
    display: str
