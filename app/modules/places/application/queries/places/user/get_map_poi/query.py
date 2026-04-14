from dataclasses import (
    dataclass,
    field,
)

from app.core.application.queries.language import LanguageMixin


@dataclass
class BBox:
    south: float
    west: float
    north: float
    east: float

    def validate(self) -> None:
        if not (-90 <= self.south <= 90 and -90 <= self.north <= 90):
            raise ValueError("Latitude out of range")

        if not (-180 <= self.west <= 180 and -180 <= self.east <= 180):
            raise ValueError("Longitude out of range")

        if self.south >= self.north:
            raise ValueError("south must be < north")

        if self.west >= self.east:
            raise ValueError("west must be < east")


@dataclass(frozen=True, slots=True, kw_only=True)
class GetPlacesMapPOIQuery(LanguageMixin):
    bounds: BBox
    limit: int = field(default=100)
