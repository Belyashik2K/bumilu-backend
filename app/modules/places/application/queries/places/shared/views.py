from dataclasses import (
    dataclass,
    field,
)
from datetime import time
from uuid import UUID

from app.core.application.queries.pagination import OffsetPagination
from app.modules.places.shared.enums import PlacePhoneTypeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceLocationView:
    latitude: float
    longitude: float


@dataclass(frozen=True, slots=True, kw_only=True)
class PlacePhoneView:
    number: str
    type: PlacePhoneTypeEnum
    primary: bool


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceAddressView:
    display: str
    taxi: str | None = field(default=None)
    taxi_comment: str | None = field(default=None)


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceWorkingHoursIntervalView:
    start: time
    end: time


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceView:
    id: UUID
    category_id: UUID
    title: str
    description: str | None = field(default=None)
    short_description: str | None = field(default=None)
    timezone: str
    location: PlaceLocationView
    address: PlaceAddressView
    phones: list[PlacePhoneView] = field(default_factory=list)
    weekly_working_hours: dict[str, list[PlaceWorkingHoursIntervalView]] = field(
        default_factory=dict
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCardCategoryView:
    name: str


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCardView:
    id: UUID
    title: str
    short_description: str | None = field(default=None)
    timezone: str
    category: PlaceCardCategoryView
    location: PlaceLocationView
    today_working_hours: list[PlaceWorkingHoursIntervalView] = field(
        default_factory=list
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCardPage:
    items: list[PlaceCardView]
    total: int


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedPlaceCardView:
    places: list[PlaceCardView] = field(default_factory=list)
    pagination: OffsetPagination


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceMapPOICategoryView:
    id: UUID
    name: str
    icon_key: str


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceMapPOIView:
    id: UUID
    title: str
    category: PlaceMapPOICategoryView
    location: PlaceLocationView
