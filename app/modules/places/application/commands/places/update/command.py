from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.constants import (
    UNSET,
    UnsetType,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdatePlaceCommand:
    place_id: UUID
    category_slug: str | UnsetType = field(default=UNSET)
    latitude: float | UnsetType = field(default=UNSET)
    longitude: float | UnsetType = field(default=UNSET)
    address_taxi: str | UnsetType = field(default=UNSET)
    address_taxi_comment: str | None | UnsetType = field(default=UNSET)
