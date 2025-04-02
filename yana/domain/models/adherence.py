from enum import Enum
from typing import Optional, Self
from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime

from yana.domain.models.schedule import Repeated, RepeatedMonthlyOn


class ScheduleType(str, Enum):
    MEDICATION = "medication"
    APPOINTMENT = "appointment"
    OTHER = "other"

    @classmethod
    def try_from_str(cls: type[Self], value: str) -> Self:
        for status in cls:
            if status.value == value.lower():
                return status
        raise ValueError(f"{value} must be a valid type")


class AdherenceStatus(str, Enum):
    FULLY_ADHERENT = "fully_adherent"
    PARTIALLY_ADHERENT = "partially_adherent"
    NOT_ADHERENT = "not_adherent"
    TEMPORARILY_EXEMPT = "temporarily_exempt"
    NOT_RELEVANT = "not_relevant"

    @classmethod
    def try_from_str(cls: type[Self], value: str) -> Self:
        for status in cls:
            if status.value == value.lower():
                return status
        raise ValueError(f"{value} must be a valid status")


class ReminderStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    ACKNOWLEDGED = "acknowledged"
    OVERDUE = "overdue"
    COMPLETED = "completed"

    @classmethod
    def try_from_str(cls: type[Self], value: str) -> Self:
        for status in cls:
            if status.value == value.lower():
                return status
        raise ValueError(f"{value} must be a valid status")


class BaseAdherenceSlotModel(BaseModel):
    datetime: DateTime
    adherence_time: Optional[DateTime] = None
    adherence_status: Optional[AdherenceStatus]
    reminder_status: Optional[ReminderStatus]
    non_adherence_reason: Optional[str]
    notes: Optional[str]
    schedule_id: str


class AdherenceSlotModel(BaseAdherenceSlotModel):
    id: str

class FullAdherenceSlotModel(AdherenceSlotModel):
    repeated: Optional[Repeated] = None
    repetition_step: int
    repeated_monthly_on: Optional[RepeatedMonthlyOn] = None
    rep_count: int = 0

class AdherenceRateModel(BaseModel):
    total_slots: int
    fully_adherent_count: int
    adherence_rate: int

