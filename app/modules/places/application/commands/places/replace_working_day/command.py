from dataclasses import (
    dataclass,
    field,
)
from datetime import time
from uuid import UUID

from app.modules.places.shared.enums.place_working_day_status import (
    PlaceWorkingDayStatusEnum,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkingDayIntervalData:
    start_time: time
    end_time: time


@dataclass(frozen=True, slots=True, kw_only=True)
class ReplacePlaceWorkingDayCommand:
    place_id: UUID
    weekday: int
    status: PlaceWorkingDayStatusEnum
    intervals: list[WorkingDayIntervalData] = field(default_factory=list)
