from dataclasses import (
    dataclass,
    field,
)

from app.modules.routing.shared.enums.travel_mode import TravelModeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class Waypoint:
    latitude: float
    longitude: float

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Waypoint):
            return NotImplemented
        return self.latitude == other.latitude and self.longitude == other.longitude


@dataclass(frozen=True, slots=True, kw_only=True)
class GetRouteQuery:
    points: list[Waypoint] = field(default_factory=list)
    mode: TravelModeEnum
