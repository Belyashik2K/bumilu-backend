from app.modules.places.application.queries.places.shared.models.place_working_hour import (
    PlaceWorkingHourReadModel,
)
from app.modules.places.application.queries.places.shared.views import (
    PlaceWorkingHoursIntervalView,
)


def group_working_hours_by_day(
    working_hours: list[PlaceWorkingHourReadModel],
) -> dict[str, list[PlaceWorkingHoursIntervalView]]:
    return {
        str(day): [
            PlaceWorkingHoursIntervalView(
                start=wh.start_time,
                end=wh.end_time,
            )
            for wh in working_hours
            if wh.weekday == day
        ]
        for day in range(1, 8)
    }
