from pydantic import BaseModel


class AppointmentModel(BaseModel):
    id: str
    reason: str
    location: str
    user_id: str

class NewAppointmentModel(AppointmentModel):
    id: str
