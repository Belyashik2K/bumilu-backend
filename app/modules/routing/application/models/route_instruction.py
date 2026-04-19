from dataclasses import (
    dataclass,
    field,
)

from app.modules.routing.shared.enums.travel_mode import TravelModeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteInstruction:
    text: str
    distance_meters: int
    duration_seconds: int
    begin_shape_index: int
    end_shape_index: int
    maneuver_type: str
    travel_mode: TravelModeEnum
    bearing_before: int | None = field(default=None)
    bearing_after: int | None = field(default=None)
