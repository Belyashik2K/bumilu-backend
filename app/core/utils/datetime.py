from datetime import (
    UTC,
    datetime,
)

import pytz


def get_current_dt() -> datetime:
    dt = datetime.now(tz=UTC)
    return dt.replace(microsecond=0)


def get_current_dt_in_timezone(timezone: str) -> datetime:
    tz = pytz.timezone(timezone)
    dt = datetime.now(tz=tz)
    return dt.replace(microsecond=0)
