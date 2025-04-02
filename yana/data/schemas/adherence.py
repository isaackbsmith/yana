from typing import Optional
from pydantic import BaseModel


class NewAdherenceSlotSchema(BaseModel):
    id: str
    datetime: int
    schedule_id: str

class AdherenceSlotSchema(NewAdherenceSlotSchema):
    adherence_time: Optional[str] = None
    adherence_status: Optional[str] = None
    reminder_status: Optional[str] = None
    non_adherence_reason: Optional[str] = None
    notes: Optional[str] = None

class FullAdherenceSlotSchema(AdherenceSlotSchema):
    repeated: Optional[str] = None
    repetition_step: int
    repeated_monthly_on: Optional[str] = None
    rep_count: int = 0

class AdherenceRateSchema(BaseModel):
    total_slots: int
    fully_adherent_count: int
    adherence_rate: int

