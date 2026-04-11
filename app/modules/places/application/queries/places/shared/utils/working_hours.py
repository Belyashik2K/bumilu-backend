from app.core.utils.datetime import get_current_dt_in_timezone
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
                start=wh.start,
                end=wh.end,
            )
            for wh in working_hours
            if wh.weekday == day
        ]
        for day in range(1, 8)
    }


def extract_today_working_hours(
    timezone: str,
    working_hours: list[PlaceWorkingHourReadModel],
) -> list[PlaceWorkingHoursIntervalView]:
    today_working_hours = []
    for wh in working_hours:
        now = get_current_dt_in_timezone(timezone)
        if wh.weekday == now.weekday() + 1:
            today_working_hours.append(
                PlaceWorkingHoursIntervalView(
                    start=wh.start,
                    end=wh.end,
                )
            )
    return today_working_hours
