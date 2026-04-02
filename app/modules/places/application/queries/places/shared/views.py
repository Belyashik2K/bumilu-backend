from dataclasses import (
    dataclass,
    field,
)
from datetime import time
from uuid import UUID

from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.application.queries.categories.shared.models.place_category import (
    LocalizedPlaceCategoryReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_address import (
    PlaceAddressReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_location import (
    PlaceLocationReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_phone import (
    PlacePhoneReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_rating import (
    PlaceRatingReadModel,
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
    address: PlaceAddressReadModel
    location: PlaceLocationReadModel
    rating: PlaceRatingReadModel
    phones: list[PlacePhoneReadModel]
    weekly_working_hours: dict[str, list[PlaceWorkingHoursIntervalView]] = field(
        default_factory=dict
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCardView:
    id: UUID
    title: str
    short_description: str | None = field(default=None)
    timezone: str
    category: LocalizedPlaceCategoryReadModel
    location: PlaceLocationReadModel
    rating: PlaceRatingReadModel
    today_working_hours: list[PlaceWorkingHoursIntervalView] = field(
        default_factory=list
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
