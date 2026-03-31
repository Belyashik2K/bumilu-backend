from dataclasses import (
    dataclass,
    field,
)
from datetime import time
from uuid import UUID

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
    working_hours: dict[int, list[PlaceWorkingHoursIntervalView]] = field(
        default_factory=dict
    )
