from dataclasses import dataclass

from app.core.domain.value_objects.id import PlacePhotoIdVO
from app.modules.places.shared.enums.place_photo_status import PlacePhotoStatusEnum


@dataclass(slots=True, kw_only=True)
class PlacePhoto:
    id: PlacePhotoIdVO
    file_key: str
    thumbnail_file_key: str | None
    status: PlacePhotoStatusEnum

    @classmethod
    def create(
        cls,
        *,
        file_key: str,
        status: PlacePhotoStatusEnum,
        thumbnail_file_key: str | None,
    ) -> "PlacePhoto":
        return cls(
            id=PlacePhotoIdVO.new(),
            file_key=file_key,
            thumbnail_file_key=thumbnail_file_key,
            status=status,
        )

    @classmethod
    def create_pending(cls, *, file_key: str) -> "PlacePhoto":
        return cls(
            id=PlacePhotoIdVO.new(),
            file_key=file_key,
            thumbnail_file_key=None,
            status=PlacePhotoStatusEnum.PENDING_UPLOAD,
        )

    def mark_uploaded(self) -> None:
        self.status = PlacePhotoStatusEnum.UPLOADED

    def mark_processing(self) -> None:
        self.status = PlacePhotoStatusEnum.PROCESSING

    def mark_ready(self, *, thumbnail_file_key: str | None) -> None:
        self.status = PlacePhotoStatusEnum.READY
        self.thumbnail_file_key = thumbnail_file_key

    def mark_failed(self) -> None:
        self.status = PlacePhotoStatusEnum.FAILED
