import pytz
from datetime import datetime
from typing import cast
import pendulum
from pydantic_extra_types.pendulum_dt import DateTime


def current_timestamp() -> int:
    return pendulum.now().int_timestamp


def to_unix_date_ts(date: DateTime) -> int:
    # Reset time to midnight
    return date.start_of("day").int_timestamp


def to_unix_time_ts(time: DateTime) -> int:
    # Return the seconds since midnight
    return time.diff(time.start_of("day")).in_seconds()


def date_from_ts(timestamp: int) -> DateTime:
    # Necessary because the pendulum maintainers haven't fixed the deprecated API
    dt = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
    return cast(DateTime, pendulum.instance(dt))


def time_from_secs(time: int) -> DateTime:
    # Little hack to get the strf representation of the time
    dt = pendulum.now().start_of("day").add(seconds=time)
    return cast(DateTime, dt)


def to_date_repr(date: DateTime) -> str:
    return date.strftime("%Y-%m-%d")

def to_time_repr(time: DateTime) -> str:
    return time.strftime("%H:%M:%S")

