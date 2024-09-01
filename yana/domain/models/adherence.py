from enum import Enum
from typing import Self
from pydantic import BaseModel


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
    date: str
    time: str
    adherence_status: AdherenceStatus
    adherence_time: str
    reminder_status: ReminderStatus
    non_adherence_reason: str
    notes: str
    schedule_id: str

