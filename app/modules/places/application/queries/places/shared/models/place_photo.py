from dataclasses import dataclass
from uuid import UUID

from app.modules.places.shared.enums.place_photo_status import PlacePhotoStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class PlacePhotoReadModel:
    file_key: str
    thumbnail_file_key: str | None


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminPlacePhotoReadModel(PlacePhotoReadModel):
    status: PlacePhotoStatusEnum
    id: UUID
