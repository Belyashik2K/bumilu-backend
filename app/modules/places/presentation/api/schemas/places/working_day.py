from pydantic import (
    BaseModel,
    Field,
)

from app.modules.places.presentation.api.schemas.places.working_hours import (
    PlaceWorkingHoursIntervalSchema,
)
from app.modules.places.shared.enums.place_working_day_status import (
    PlaceWorkingDayStatusEnum,
)


class PlaceWorkingDaySchema(BaseModel):
    status: PlaceWorkingDayStatusEnum = Field(
        ...,
        description=(
            "The working day status. It determines whether the place is open, closed, "
            "or has unspecified working hours on a specific weekday."
        ),
        examples=[PlaceWorkingDayStatusEnum.OPEN],
    )
    intervals: list[PlaceWorkingHoursIntervalSchema] = Field(
        default_factory=list,
        description=(
            "The list of working intervals for the day. It should be empty when the status is "
            "UNSPECIFIED, CLOSED, or ALL_DAY, and should not be empty when the status is OPEN."
        ),
    )
