from pydantic import (
    BaseModel,
    Field,
)

NORTH_EXAMPLE = 59.943482
SOUTH_EXAMPLE = 59.934500
EAST_EXAMPLE = 30.324417
WEST_EXAMPLE = 30.306529


class RouteBoundsSchema(BaseModel):
    north: float = Field(
        ...,
        description="Northernmost latitude of the route bounds.",
        examples=[NORTH_EXAMPLE],
    )
    south: float = Field(
        ...,
        description="Southernmost latitude of the route bounds.",
        examples=[SOUTH_EXAMPLE],
    )
    east: float = Field(
        ...,
        description="Easternmost longitude of the route bounds.",
        examples=[EAST_EXAMPLE],
    )
    west: float = Field(
        ...,
        description="Westernmost longitude of the route bounds.",
        examples=[WEST_EXAMPLE],
    )
