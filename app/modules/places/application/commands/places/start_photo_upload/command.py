from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class StartPlacePhotoUploadCommand:
    place_id: UUID
    content_type: str


@dataclass(frozen=True, slots=True, kw_only=True)
class StartPlacePhotoUploadCommandResult:
    photo_id: UUID
    file_key: str
    upload_url: str
