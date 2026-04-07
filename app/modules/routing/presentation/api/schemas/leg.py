from pydantic import (
    BaseModel,
    Field,
)

from app.modules.routing.presentation.api.schemas.geometry import RouteGeometrySchema
from app.modules.routing.presentation.api.schemas.instruction import (
    RouteInstructionSchema,
)

DISTANCE_METERS_EXAMPLE = 1500
DURATION_SECONDS_EXAMPLE = 300


class RouteLegSchema(BaseModel):
    distance_meters: int = Field(
        ...,
        description="The total distance of the leg in meters.",
        examples=[DISTANCE_METERS_EXAMPLE],
    )
    duration_seconds: int = Field(
        ...,
        description="The total duration of the leg in seconds.",
        examples=[DURATION_SECONDS_EXAMPLE],
    )
    geometry: RouteGeometrySchema = Field(
        ...,
        description="The geometry of the leg, which includes the format and the encoded geometry string.",
    )
    instructions: list[RouteInstructionSchema] = Field(
        ...,
        description="A list of instructions for navigating the leg. Each instruction includes details such as the text, distance, duration, and maneuver type.",
    )
