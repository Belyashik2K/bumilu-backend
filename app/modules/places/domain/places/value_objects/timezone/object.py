from dataclasses import dataclass
from typing import Self
from zoneinfo import (
    ZoneInfo,
    ZoneInfoNotFoundError,
)

from app.core.domain.value_objects.location import LocationVO
from app.core.utils.datetime import get_timezone_by_coordinates
from app.modules.places.domain.places.value_objects.timezone.exceptions import (
    InvalidTimezone,
)


@dataclass(frozen=True, slots=True)
class TimezoneVO:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise InvalidTimezone(
                message="Timezone cannot be empty", timezone=self.value
            )

        try:
            ZoneInfo(self.value)
        except ZoneInfoNotFoundError as e:
            raise InvalidTimezone(
                message="Timezone does not exist", timezone=self.value
            ) from e

    @classmethod
    def from_coordinates(cls, latitude: float, longitude: float) -> Self:
        return cls(get_timezone_by_coordinates(latitude=latitude, longitude=longitude))

    @classmethod
    def from_location(cls, location: LocationVO) -> Self:
        return cls.from_coordinates(
            latitude=location.latitude, longitude=location.longitude
        )

    @property
    def tzinfo(self) -> ZoneInfo:
        return ZoneInfo(self.value)
