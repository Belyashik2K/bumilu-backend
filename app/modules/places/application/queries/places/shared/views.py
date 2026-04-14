from dataclasses import (
    dataclass,
    field,
)
from typing import Self
from uuid import UUID

from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.places.application.queries.categories.shared.models.place_category import (
    LocalizedPlaceCategoryReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_address import (
    PlaceAddressReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_card import (
    PlaceCardReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_location import (
    PlaceLocationReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_phone import (
    PlacePhoneReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_photo import (
    PlacePhotoReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_rating import (
    PlaceRatingReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_user_context import (
    PlaceUserContextReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_working_day import (
    PlaceWorkingDayReadModel,
)
from app.modules.places.shared.enums.place_photo_status import PlacePhotoStatusEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class PlacePhotoView:
    url: str
    thumbnail_url: str | None = field(default=None)
    status: PlacePhotoStatusEnum

    @classmethod
    def from_read_model(
        cls,
        read_model: PlacePhotoReadModel,
        storage_url_builder: IFileStorageURLBuilder,
    ) -> Self:
        return cls(
            url=storage_url_builder.build_file_url(file_key=read_model.file_key),
            thumbnail_url=storage_url_builder.build_file_url(
                file_key=read_model.thumbnail_file_key
            ),
            status=read_model.status,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceView:
    id: UUID
    title: str
    description: str | None = field(default=None)
    short_description: str | None = field(default=None)
    timezone: str
    category: LocalizedPlaceCategoryReadModel
    photos: list[PlacePhotoView] = field(default_factory=list)
    address: PlaceAddressReadModel
    location: PlaceLocationReadModel
    rating: PlaceRatingReadModel
    phones: list[PlacePhoneReadModel] = field(default_factory=list)
    working_days: list[PlaceWorkingDayReadModel] = field(default_factory=list)
    user_context: PlaceUserContextReadModel


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCardView:
    id: UUID
    title: str
    short_description: str | None = field(default=None)
    timezone: str
    category: LocalizedPlaceCategoryReadModel
    photos: list[PlacePhotoView] = field(default_factory=list)
    location: PlaceLocationReadModel
    rating: PlaceRatingReadModel
    working_days: list[PlaceWorkingDayReadModel] = field(default_factory=list)

    @classmethod
    def from_read_model(
        cls,
        read_model: PlaceCardReadModel,
        storage_url_builder: IFileStorageURLBuilder,
    ) -> Self:
        # TODO: configurable number of photos

        return PlaceCardView(
            id=read_model.id,
            title=read_model.title,
            short_description=read_model.short_description,
            timezone=read_model.timezone,
            category=read_model.category,
            photos=[
                PlacePhotoView.from_read_model(
                    read_model=photo,
                    storage_url_builder=storage_url_builder,
                )
                for photo in read_model.photos[:4]
            ],
            location=read_model.location,
            rating=read_model.rating,
            working_days=read_model.working_days,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedPlaceCardView:
    places: list[PlaceCardView] = field(default_factory=list)
    pagination: OffsetPagination


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceMapPOICategoryView:
    id: UUID
    name: str
    icon_key: str
    marker_color: str


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceMapPOIView:
    id: UUID
    title: str
    category: PlaceMapPOICategoryView
    location: PlaceLocationReadModel
