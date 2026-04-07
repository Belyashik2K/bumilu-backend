from collections.abc import Sequence
from dataclasses import (
    dataclass,
    field,
)

from app.modules.routing.application.models.route_geometry import RouteGeometry
from app.modules.routing.application.models.route_instruction import RouteInstruction


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteLeg:
    distance_meters: int
    duration_seconds: int
    geometry: RouteGeometry
    instructions: Sequence[RouteInstruction] = field(default_factory=tuple)
