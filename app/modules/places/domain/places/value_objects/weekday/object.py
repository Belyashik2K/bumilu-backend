from dataclasses import dataclass

from app.modules.places.domain.places.value_objects.weekday.exceptions import (
    InvalidWeekday,
)


@dataclass(frozen=True, slots=True)
class WeekdayVO:
    value: int

    def __post_init__(self) -> None:
        if self.value < 1 or self.value > 7:
            raise InvalidWeekday(weekday=self.value)
