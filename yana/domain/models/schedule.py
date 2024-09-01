from enum import Enum
from typing import Optional, Self
from pydantic import BaseModel, Field
from pydantic_extra_types.pendulum_dt import DateTime

from yana.domain.models import DOW

class Repeated(str, Enum):
    MINUTELY = "minutely"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ANNUALLY = "annually"

    @classmethod
    def try_from_str(cls: type[Self], value: str) -> Self:
        for repeated in cls:
            if repeated.value == value.lower():
                return repeated
        raise ValueError(f"{value} must be a valid repeated")

class RepeatedMonthlyOn(str, Enum):
    SAME_DAY = "same_day"
    SAME_WEEKDAY = "same_weekday"

    @classmethod
    def try_from_str(cls: type[Self], value: str) -> Self:
        for repeated in cls:
            if repeated.value == value.lower():
                return repeated
        raise ValueError(f"{value} must be a valid repeated")

class RepeatedUntil(str, Enum):
    FOREVER = "forever"
    UNTIL_DATE = "until_date"
    N_REPETITIONS = "n_repetitions"

    @classmethod
    def try_from_str(cls: type[Self], value: str) -> Self:
        for repeated in cls:
            if repeated.value == value.lower():
                return repeated
        raise ValueError(f"{value} must be a valid repeated")


class BaseScheduleModel(BaseModel):
    begin_date: DateTime
    end_date: DateTime
    begin_time: DateTime
    end_time: Optional[DateTime] = None
    schedule_type: str
    user_id: str
    medication_id: Optional[str] = None
    appointment_id: Optional[str] = None


class NewScheduleModel(BaseScheduleModel):
    repeated: Optional[Repeated] = None
    repetition_step: int = 0
    repeated_until: Optional[RepeatedUntil] = None
    repeated_monthly_on: Optional[RepeatedMonthlyOn] = None
    repeated_until_date: Optional[DateTime] = None
    repeated_reps: Optional[int] = None
    days_of_week: list[DOW] = Field(default_factory=list)


class ScheduleModel(NewScheduleModel):
    id: str


class RepeatedScheduleModel(BaseScheduleModel):
    id: str
    repeated: Repeated
    repetition_step: int
    repeated_until: RepeatedUntil


class MonthlyRepeatedScheduleModel(RepeatedScheduleModel):
    repeated_monthly_on: RepeatedMonthlyOn


class RepeatedUntilDateScheduleModel(RepeatedScheduleModel):
    repeated_until_date: DateTime


class NRepetitionsScheduleModel(RepeatedScheduleModel):
    repeated_reps: int

