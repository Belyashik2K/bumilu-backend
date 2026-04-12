from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class DeletePlacePhotoCommand:
    place_id: UUID
    photo_id: UUID
