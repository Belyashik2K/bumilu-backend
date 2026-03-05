from dataclasses import dataclass
from typing import Final

from app.modules.chat.domain.value_objects.location.exceptions import (
    InvalidLatitude,
    InvalidLongitude,
)

MINIMUM_LATITUDE: Final[float] = -90.0
MAXIMUM_LATITUDE: Final[float] = 90.0

MINIMUM_LONGITUDE: Final[float] = -180.0
MAXIMUM_LONGITUDE: Final[float] = 180.0


@dataclass(frozen=True, slots=True, kw_only=True)
class LocationVO:
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not self.latitude or not (-90 <= self.latitude <= 90):
            raise InvalidLatitude(
                latitude=self.latitude,
                min_value=MINIMUM_LATITUDE,
                max_value=MAXIMUM_LATITUDE,
            )

        if not self.longitude or not (-180 <= self.longitude <= 180):
            raise InvalidLongitude(
                longitude=self.longitude,
                min_value=MINIMUM_LONGITUDE,
                max_value=MAXIMUM_LONGITUDE,
            )
