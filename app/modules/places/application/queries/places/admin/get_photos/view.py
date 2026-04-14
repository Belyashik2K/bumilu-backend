from dataclasses import (
    dataclass,
    field,
)
from typing import Self
from uuid import UUID

from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.places.application.queries.places.shared.models.place_photo import (
    AdminPlacePhotoReadModel,
)
from app.modules.places.shared.enums.place_photo_status import PlacePhotoStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminPlacePhotoView:
    id: UUID
    url: str
    thumbnail_url: str | None = field(default=None)
    status: PlacePhotoStatusEnum

    @classmethod
    def from_read_model(
        cls,
        read_model: AdminPlacePhotoReadModel,
        storage_url_builder: IFileStorageURLBuilder,
    ) -> Self:
        return cls(
            id=read_model.id,
            url=storage_url_builder.build_file_url(file_key=read_model.file_key),
            thumbnail_url=storage_url_builder.build_file_url(
                file_key=read_model.thumbnail_file_key
            ),
            status=read_model.status,
        )
