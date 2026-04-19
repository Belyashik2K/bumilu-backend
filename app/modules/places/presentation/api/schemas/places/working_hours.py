from datetime import time

from pydantic import (
    BaseModel,
    Field,
)

from app.modules.places.presentation.api.schemas.places.examples import (
    END_TIME_EXAMPLE,
    START_TIME_EXAMPLE,
)


class PlaceWorkingHoursIntervalSchema(BaseModel):
    start: time = Field(
        ...,
        description="Start time of the working hours interval",
        examples=[START_TIME_EXAMPLE],
    )
    end: time = Field(
        ...,
        description="End time of the working hours interval",
        examples=[END_TIME_EXAMPLE],
    )
