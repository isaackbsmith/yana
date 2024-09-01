from enum import Enum
from typing import Self


class DOW(str, Enum):
    MONDAY = "mon"
    TUESDAY = "tue"
    WEDNESDAY = "wed"
    THURSDAY = "thu"
    FRIDAY = "fri"
    SATURDAY = "sat"
    SUNDAY = "sun"

    @classmethod
    def try_from_str(cls: type[Self], value: str) -> Self:
        for dow in cls:
            if dow.value == value.lower():
                return dow
        raise ValueError(f"{value} must be a valid day of the week")

