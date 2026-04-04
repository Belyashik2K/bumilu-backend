from dataclasses import (
    dataclass,
    field,
)
from datetime import time
from typing import Self
from uuid import UUID

from app.core.application.queries.pagination import OffsetPagination
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


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceWorkingHoursIntervalView:
    start: time
    end: time


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceView:
    id: UUID
    title: str
    description: str | None = field(default=None)
    short_description: str | None = field(default=None)
    timezone: str
    category: LocalizedPlaceCategoryReadModel
    photos: list[PlacePhotoReadModel] = field(default_factory=list)
    address: PlaceAddressReadModel
    location: PlaceLocationReadModel
    rating: PlaceRatingReadModel
    phones: list[PlacePhoneReadModel] = field(default_factory=list)
    weekly_working_hours: dict[str, list[PlaceWorkingHoursIntervalView]] = field(
        default_factory=dict
    )
    user_context: PlaceUserContextReadModel


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCardView:
    id: UUID
    title: str
    short_description: str | None = field(default=None)
    timezone: str
    category: LocalizedPlaceCategoryReadModel
    photos: list[PlacePhotoReadModel] = field(default_factory=list)
    location: PlaceLocationReadModel
    rating: PlaceRatingReadModel
    today_working_hours: list[PlaceWorkingHoursIntervalView] = field(
        default_factory=list
    )

    @classmethod
    def from_read_model(
        cls,
        read_model: PlaceCardReadModel,
    ) -> Self:
        # TODO: configurable number of photos
        from app.modules.places.application.queries.places.shared.utils.working_hours import (
            extract_today_working_hours,
        )

        return PlaceCardView(
            id=read_model.id,
            title=read_model.title,
            short_description=read_model.short_description,
            timezone=read_model.timezone,
            category=read_model.category,
            photos=read_model.photos[:4],
            location=read_model.location,
            rating=read_model.rating,
            today_working_hours=extract_today_working_hours(
                timezone=read_model.timezone,
                working_hours=read_model.working_hours,
            ),
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
