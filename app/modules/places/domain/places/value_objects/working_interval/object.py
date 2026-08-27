from dataclasses import dataclass
from datetime import time

from app.modules.places.domain.places.value_objects.working_interval.exceptions import (
    InvalidWorkingInterval,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkingIntervalVO:
    start_time: time
    end_time: time

    def __post_init__(self) -> None:
        if self.start_time >= self.end_time:
            raise InvalidWorkingInterval(
                start_time=self.start_time,
                end_time=self.end_time,
            )

    def __str__(self) -> str:
        return f"{self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"
