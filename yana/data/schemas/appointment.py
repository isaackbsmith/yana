from pydantic import BaseModel


class AppointmentSchema(BaseModel):
    id: str
    reason: str
    location: str
    # user_id: str
