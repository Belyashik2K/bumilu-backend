from pydantic import (
    BaseModel,
    Field,
)

LATITUDE_EXAMPLE = 60.002598
LONGITUDE_EXAMPLE = 30.330861


class RouteWaypointSchema(BaseModel):
    latitude: float = Field(
        ...,
        description="Latitude of the waypoint",
        examples=[LATITUDE_EXAMPLE],
    )
    longitude: float = Field(
        ...,
        description="Longitude of the waypoint",
        examples=[LONGITUDE_EXAMPLE],
    )
