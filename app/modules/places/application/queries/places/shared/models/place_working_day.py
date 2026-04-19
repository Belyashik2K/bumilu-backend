from dataclasses import (
    dataclass,
    field,
)

from app.modules.places.application.queries.places.shared.models.place_working_hour import (
    PlaceWorkingHourReadModel,
)
from app.modules.places.shared.enums.place_working_day_status import (
    PlaceWorkingDayStatusEnum,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceWorkingDayReadModel:
    weekday: int
    status: PlaceWorkingDayStatusEnum
    intervals: list[PlaceWorkingHourReadModel] = field(default_factory=list)
