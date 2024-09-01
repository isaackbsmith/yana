from typing import Optional
from pydantic import BaseModel


class BaseScheduleSchema(BaseModel):
    id: str
    begin_date: int
    end_date: int
    begin_time: int
    end_time: Optional[int] = None
    schedule_type: str
    user_id: str
    medication_id: Optional[str] = None
    appointment_id: Optional[str] = None


class ScheduleSchema(BaseScheduleSchema):
    repeated: Optional[str] = None
    repetition_step: int = 0
    repeated_until: Optional[str] = None
    repeated_monthly_on: Optional[str] = None
    repeated_until_date: Optional[int] = None
    repeated_reps: Optional[int] = None


class RepeatedScheduleSchema(BaseScheduleSchema):
    repeated: str
    repetition_step: int
    repeated_until: str


class MonthlyRepeatedSchedulSchema(RepeatedScheduleSchema):
    repeated_monthly_on: str


class RepeatedUntilDateScheduleModel(RepeatedScheduleSchema):
    repeated_until_date: int


class NRepetitionsScheduleModel(RepeatedScheduleSchema):
    repeated_reps: int

