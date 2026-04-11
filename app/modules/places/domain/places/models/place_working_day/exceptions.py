from app.core.exceptions.domain.base import (
    DomainConflictException,
    DomainValidationException,
)
from app.modules.places.domain.places.value_objects.weekday.object import WeekdayVO
from app.modules.places.domain.places.value_objects.working_interval.object import (
    WorkingIntervalVO,
)
from app.modules.places.shared.enums.place_working_day_status import (
    PlaceWorkingDayStatusEnum,
)


class DuplicateWorkingInterval(DomainConflictException):
    def __init__(
        self,
        weekday: WeekdayVO,
        interval: WorkingIntervalVO,
    ) -> None:
        super().__init__(
            message=(
                f"Working interval {interval} for weekday {weekday} already exists."
            )
        )


class InvalidPlaceWorkingDayState(DomainValidationException):
    def __init__(self, weekday: WeekdayVO, status: PlaceWorkingDayStatusEnum) -> None:
        message = (
            f"Invalid state for place working day with weekday {weekday} and status {status}. "
            f"Intervals should be empty when status is in "
            f"{{{PlaceWorkingDayStatusEnum.UNSPECIFIED}, "
            f"{PlaceWorkingDayStatusEnum.CLOSED}, "
            f"{PlaceWorkingDayStatusEnum.ALL_DAY}}}, "
            f"and should not be empty when status is {PlaceWorkingDayStatusEnum.OPEN}."
        )

        super().__init__(message=message)


class WorkingIntervalsOverlap(DomainValidationException):
    def __init__(
        self,
        weekday: WeekdayVO,
        interval1: WorkingIntervalVO,
        interval2: WorkingIntervalVO,
    ) -> None:
        super().__init__(
            message=(
                f"Working intervals {interval1} and {interval2} for weekday {weekday} overlap."
            )
        )


class UnsupportedPlaceWorkingDayStatus(DomainValidationException):
    def __init__(self, status: PlaceWorkingDayStatusEnum) -> None:
        super().__init__(message=(f"Unsupported place working day status: {status}."))
