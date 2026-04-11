from dataclasses import (
    dataclass,
    field,
)
from uuid import UUID

from app.core.constants import (
    UNSET,
    UnsetType,
)
from app.modules.places.shared.enums import PlacePhoneTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdatePlacePhoneCommand:
    place_id: UUID
    phone_id: UUID
    number: str | UnsetType = field(default=UNSET)
    type: PlacePhoneTypeEnum | UnsetType = field(default=UNSET)
