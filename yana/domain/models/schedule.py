from enum import Enum
from typing import Annotated, Any, Optional, Self
from pydantic import BaseModel, Field, PlainSerializer, model_serializer
from pydantic_extra_types.pendulum_dt import DateTime

from yana.domain.models import DOW
from yana.utils.datetime import to_date_repr, to_time_repr


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


# Custom serializers
YANADate = Annotated[DateTime, PlainSerializer(lambda x: to_date_repr(x), return_type=str, when_used="json")]
YANATime = Annotated[DateTime, PlainSerializer(lambda x: to_time_repr(x), return_type=str, when_used="json")]


class BaseScheduleModel(BaseModel):
    begin_date: YANADate
    end_date: Optional[YANADate]
    begin_time: YANATime
    end_time: Optional[YANATime] = None
    schedule_type: str
    # user_id: str


class NewScheduleModel(BaseScheduleModel):
    repeated: Optional[Repeated] = None
    repetition_step: int = 0
    repeated_until: Optional[RepeatedUntil] = None
    repeated_monthly_on: Optional[RepeatedMonthlyOn] = None
    repeated_until_date: Optional[YANADate] = None
    repeated_reps: Optional[int] = None
    days_of_week: list[DOW] = Field(default_factory=list)
    medication_id: Optional[str] = None
    appointment_id: Optional[str] = None


class ScheduleModel(NewScheduleModel):
    id: str
    medication: Optional[str] = None
    appointment: Optional[str] = None


class RepeatedScheduleModel(BaseScheduleModel):
    id: str
    repeated: Repeated
    repetition_step: int
    repeated_until: RepeatedUntil
    medication: Optional[str] = None
    appointment: Optional[str] = None

class ScheduleMedicationModel(BaseModel):
    name: str

class MonthlyRepeatedScheduleModel(RepeatedScheduleModel):
    repeated_monthly_on: RepeatedMonthlyOn


class RepeatedUntilDateScheduleModel(RepeatedScheduleModel):
    repeated_until_date: YANADate


class NRepetitionsScheduleModel(RepeatedScheduleModel):
    repeated_reps: int
