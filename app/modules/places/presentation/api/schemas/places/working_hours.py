from datetime import time

from pydantic import (
    BaseModel,
    Field,
)

START_TIME_EXAMPLE = time(0, 0, 0)
END_TIME_EXAMPLE = time(23, 59, 59)


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
