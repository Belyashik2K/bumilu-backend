from datetime import (
    UTC,
    datetime,
)
from functools import lru_cache
from zoneinfo import ZoneInfo

from timezonefinder import timezonefinder

tf = timezonefinder.TimezoneFinder()


def get_current_dt() -> datetime:
    dt = datetime.now(tz=UTC)
    return dt.replace(microsecond=0)


def get_current_dt_in_timezone(timezone: str) -> datetime:
    tz = ZoneInfo(timezone)
    dt = datetime.now(tz=tz)
    return dt.replace(microsecond=0)


@lru_cache(maxsize=10_000)
def get_timezone_by_coordinates(latitude: float, longitude: float) -> str | None:
    return tf.timezone_at(lng=longitude, lat=latitude)
