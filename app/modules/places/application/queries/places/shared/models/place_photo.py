from dataclasses import dataclass

from app.modules.places.shared.enums.place_photo_status import PlacePhotoStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class PlacePhotoReadModel:
    file_key: str
    thumbnail_file_key: str
    status: PlacePhotoStatusEnum
