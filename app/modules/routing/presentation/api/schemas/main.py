from pydantic import (
    BaseModel,
    Field,
)

from app.modules.routing.presentation.api.schemas.waypoint import RouteWaypointSchema
from app.modules.routing.shared.enums.travel_mode import TravelModeEnum


class GetRouteBetweenPointsRequestSchema(BaseModel):
    waypoints: list[RouteWaypointSchema] = Field(
        ...,
        description="List of waypoints that define the route. Each waypoint should include latitude and longitude.",
    )
    travel_mode: TravelModeEnum = Field(
        ..., description="Travel mode for the route.", examples=[TravelModeEnum.WALK]
    )
