from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.modules.places.shared.enums import PlacePhoneTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPlacePhoneCommand:
    place_id: UUID
    number: str
    type: PlacePhoneTypeEnum
    is_primary: bool = field(default=False)
