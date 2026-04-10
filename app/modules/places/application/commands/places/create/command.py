from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePlaceCommand:
    category_slug: str
    latitude: float
    longitude: float
    address_taxi: str
    address_taxi_comment: str | None = field(default=None)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePlaceCommandResult:
    id: UUID
