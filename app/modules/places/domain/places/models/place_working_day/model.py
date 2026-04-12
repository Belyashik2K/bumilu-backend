from dataclasses import (
    dataclass,
    field,
)
from datetime import time
from typing import Self

from app.core.domain.value_objects.id import PlaceWorkingDayIdVO
from app.modules.places.domain.places.models.place_working_day.exceptions import (
    DuplicateWorkingInterval,
    InvalidPlaceWorkingDayState,
    UnsupportedPlaceWorkingDayStatus,
    WorkingIntervalsOverlap,
)
from app.modules.places.domain.places.value_objects.weekday.object import WeekdayVO
from app.modules.places.domain.places.value_objects.working_interval.object import (
    WorkingIntervalVO,
)
from app.modules.places.shared.enums.place_working_day_status import (
    PlaceWorkingDayStatusEnum,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceWorkingDayData:
    weekday: WeekdayVO
    status: PlaceWorkingDayStatusEnum
    intervals: list[WorkingIntervalVO] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class PlaceWorkingDay:
    id: PlaceWorkingDayIdVO
    weekday: WeekdayVO
    status: PlaceWorkingDayStatusEnum
    intervals: list[WorkingIntervalVO] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate()

    @classmethod
    def create(
        cls,
        *,
        weekday: WeekdayVO,
        status: PlaceWorkingDayStatusEnum,
        intervals: list[WorkingIntervalVO],
    ) -> Self:
        return cls(
            id=PlaceWorkingDayIdVO.new(),
            weekday=weekday,
            status=status,
            intervals=intervals,
        )

    def is_unspecified(self) -> bool:
        return self.status == PlaceWorkingDayStatusEnum.UNSPECIFIED

    def is_closed(self) -> bool:
        return self.status == PlaceWorkingDayStatusEnum.CLOSED

    def is_all_day(self) -> bool:
        return self.status == PlaceWorkingDayStatusEnum.ALL_DAY

    def is_open(self) -> bool:
        return self.status == PlaceWorkingDayStatusEnum.OPEN

    def replace_with_unspecified(self) -> None:
        self.status = PlaceWorkingDayStatusEnum.UNSPECIFIED
        self.intervals = []
        self._validate()

    def replace_with_closed(self) -> None:
        self.status = PlaceWorkingDayStatusEnum.CLOSED
        self.intervals = []
        self._validate()

    def replace_with_all_day(self) -> None:
        self.status = PlaceWorkingDayStatusEnum.ALL_DAY
        self.intervals = []
        self._validate()

    def replace_with_open(
        self,
        *,
        intervals: list[WorkingIntervalVO],
    ) -> None:
        self.status = PlaceWorkingDayStatusEnum.OPEN
        self.intervals = intervals
        self._validate()

    def _validate(self) -> None:
        if self.status in {
            PlaceWorkingDayStatusEnum.UNSPECIFIED,
            PlaceWorkingDayStatusEnum.CLOSED,
            PlaceWorkingDayStatusEnum.ALL_DAY,
        }:
            if self.intervals:
                raise InvalidPlaceWorkingDayState(
                    weekday=self.weekday,
                    status=self.status,
                )
            return

        if self.status == PlaceWorkingDayStatusEnum.OPEN:
            if not self.intervals:
                raise InvalidPlaceWorkingDayState(
                    weekday=self.weekday,
                    status=self.status,
                )

            sorted_intervals = sorted(
                self.intervals,
                key=lambda interval: interval.start_time,
            )

            unique_intervals: set[tuple[time, time]] = set()
            previous: WorkingIntervalVO | None = None

            for interval in sorted_intervals:
                key = (interval.start_time, interval.end_time)
                if key in unique_intervals:
                    raise DuplicateWorkingInterval(
                        weekday=self.weekday,
                        interval=interval,
                    )
                unique_intervals.add(key)

                if previous is not None and previous.end_time > interval.start_time:
                    raise WorkingIntervalsOverlap(
                        weekday=self.weekday,
                        interval1=previous,
                        interval2=interval,
                    )

                previous = interval
            return

        raise UnsupportedPlaceWorkingDayStatus(status=self.status)
