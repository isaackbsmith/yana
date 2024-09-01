from typing import cast
import pendulum
from pydantic_extra_types.pendulum_dt import DateTime


def from_ts(timestamp: int) -> DateTime:
    return cast(DateTime, pendulum.from_timestamp(timestamp))

def to_iso8601(timestamp: int) -> str:
    return pendulum.from_timestamp(timestamp).to_iso8601_string()
