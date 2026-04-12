from dataclasses import dataclass
from uuid import UUID

from app.modules.places.shared.enums.place_status import PlaceStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangePlaceStatusCommand:
    place_id: UUID
    status: PlaceStatusEnum
