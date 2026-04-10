from dataclasses import dataclass
from typing import (
    Final,
    Self,
)

from app.core.domain.value_objects.location.exceptions import (
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
        if self.latitude is None or not (-90 <= self.latitude <= 90):
            raise InvalidLatitude(
                latitude=self.latitude,
                min_value=MINIMUM_LATITUDE,
                max_value=MAXIMUM_LATITUDE,
            )

        if self.longitude is None or not (-180 <= self.longitude <= 180):
            raise InvalidLongitude(
                longitude=self.longitude,
                min_value=MINIMUM_LONGITUDE,
                max_value=MAXIMUM_LONGITUDE,
            )

    @classmethod
    def from_coordinates(
        cls, latitude: float | None, longitude: float | None
    ) -> Self | None:
        if latitude is None or longitude is None:
            return None
        return cls(latitude=latitude, longitude=longitude)
