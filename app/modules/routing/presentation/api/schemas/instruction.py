from pydantic import (
    BaseModel,
    Field,
)

from app.modules.routing.shared.enums.travel_mode import TravelModeEnum

TEXT_EXAMPLE = "Вы прибыли в пункт назначения."
DISTANCE_METERS_EXAMPLE = 150
DURATION_SECONDS_EXAMPLE = 120
BEGIN_SHAPE_INDEX_EXAMPLE = 0
END_SHAPE_INDEX_EXAMPLE = 5
MANEUVER_TYPE_EXAMPLE = "arrive"
TRAVEL_MODE_EXAMPLE = "walk"
BEARING_BEFORE_EXAMPLE = 90
BEARING_AFTER_EXAMPLE = 180


class RouteInstructionSchema(BaseModel):
    text: str = Field(
        ...,
        description="Instruction text for the maneuver.",
        examples=[TEXT_EXAMPLE],
    )
    distance_meters: int = Field(
        ...,
        description="Distance in meters for this instruction.",
        examples=[DISTANCE_METERS_EXAMPLE],
    )
    duration_seconds: int = Field(
        ...,
        description="Duration in seconds for this instruction.",
        examples=[DURATION_SECONDS_EXAMPLE],
    )
    begin_shape_index: int = Field(
        ...,
        description="Index of the shape where this instruction begins.",
        examples=[BEGIN_SHAPE_INDEX_EXAMPLE],
    )
    end_shape_index: int = Field(
        ...,
        description="Index of the shape where this instruction ends.",
        examples=[END_SHAPE_INDEX_EXAMPLE],
    )
    maneuver_type: str = Field(
        ...,
        description="Type of maneuver. It is int, parsed as string.",
        examples=[MANEUVER_TYPE_EXAMPLE],
    )
    travel_mode: TravelModeEnum = Field(
        ...,
        description="Travel mode for this instruction.",
        examples=[TRAVEL_MODE_EXAMPLE],
    )
    bearing_before: int | None = Field(
        None,
        description="Bearing before the maneuver, in degrees. Optional.",
        examples=[BEARING_BEFORE_EXAMPLE],
    )
    bearing_after: int | None = Field(
        None,
        description="Bearing after the maneuver, in degrees. Optional.",
        examples=[BEARING_AFTER_EXAMPLE],
    )
