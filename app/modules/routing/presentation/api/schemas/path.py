from pydantic import (
    BaseModel,
    Field,
)

from app.modules.routing.presentation.api.schemas.bounds import RouteBoundsSchema
from app.modules.routing.presentation.api.schemas.geometry import RouteGeometrySchema
from app.modules.routing.presentation.api.schemas.leg import RouteLegSchema
from app.modules.routing.shared.enums.travel_mode import TravelModeEnum

DISTANCE_METERS_EXAMPLE = 1500
DURATION_SECONDS_EXAMPLE = 900


class RoutePathSchema(BaseModel):
    mode: TravelModeEnum = Field(
        ..., description="Travel mode for this path.", examples=[TravelModeEnum.WALK]
    )
    distance_meters: int = Field(
        ...,
        description="Total distance of the path in meters.",
        examples=[DISTANCE_METERS_EXAMPLE],
    )
    duration_seconds: int = Field(
        ...,
        description="Total duration of the path in seconds.",
        examples=[DURATION_SECONDS_EXAMPLE],
    )
    geometry: RouteGeometrySchema = Field(
        ...,
        description="Geometry of the path, represented as a polyline string.",
    )
    bounds: RouteBoundsSchema | None = Field(
        None,
        description="Bounding box of the path. Optional.",
    )
    legs: list[RouteLegSchema] = Field(
        default_factory=list,
        description="List of legs for this path. Each leg represents a segment of the route between waypoints.",
    )
