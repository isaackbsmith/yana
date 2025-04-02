from pydantic import BaseModel


class BaseAppointmentModel(BaseModel):
    reason: str
    location: str
    # user_id: str


class FullAppointmentModel(BaseAppointmentModel):
    id: str
