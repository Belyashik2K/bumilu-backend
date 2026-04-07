from collections.abc import Sequence
from dataclasses import (
    dataclass,
    field,
)

from app.modules.routing.application.models.route_bounds import RouteBounds
from app.modules.routing.application.models.route_geometry import RouteGeometry
from app.modules.routing.application.models.route_leg import RouteLeg
from app.modules.routing.shared.enums.travel_mode import TravelModeEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class RoutePath:
    mode: TravelModeEnum
    distance_meters: int
    duration_seconds: int
    geometry: RouteGeometry
    bounds: RouteBounds | None = field(default=None)
    legs: Sequence[RouteLeg] = field(default_factory=tuple)
