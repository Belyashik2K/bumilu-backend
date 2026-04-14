from pydantic import (
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import make_data_list_response_schema
from app.modules.places.presentation.api.schemas.places.working_hours import (
    PlaceWorkingHoursIntervalSchema,
)
from app.modules.places.shared.enums.place_working_day_status import (
    PlaceWorkingDayStatusEnum,
)


class ReplacePlaceWorkingDaySchema(BaseModel):
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


class PlaceWorkingDaySchema(ReplacePlaceWorkingDaySchema):
    weekday: int = Field(
        ...,
        description=(
            "The weekday for which the working day information is provided. It should be an integer "
            "representing the day of the week, where 1 corresponds to Monday and 7 corresponds to Sunday."
        ),
        examples=[1],
        ge=1,
        le=7,
    )


PlaceWorkingDayListResponseSchema = make_data_list_response_schema(
    item_type=PlaceWorkingDaySchema,
    description="Response schema for a list of working days for a place",
)
