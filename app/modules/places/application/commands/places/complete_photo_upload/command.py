from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class CompletePlacePhotoUploadCommand:
    place_id: UUID
    photo_id: UUID
