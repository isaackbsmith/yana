from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from yana.domain.exceptions import ServiceError
from yana.domain.models.appointment import AppointmentModel, NewAppointmentModel
from yana.service.appointments import create_appointment, fetch_appointment, modify_appointment, remove_appointment
from yana.web.exceptions import InternalServerError
from yana.web.types import Config


router = APIRouter(
    prefix="/appointments",
    tags=["appointments"]
)


@router.get("/")
async def home() -> str:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This endpoint is not allowed")


@router.post("/new")
async def new_appointment(config: Config, appointment: NewAppointmentModel):
    try:
        await create_appointment(config, appointment)
        return {"message": "Appointment created successfully"}
    except ServiceError:
        raise InternalServerError


@router.get("/{appointment_id}")
async def get_appointment(config: Config, appointment_id: str):
    try:
        user = await fetch_appointment(config, appointment_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment does not exist")
        return user
    except ServiceError:
        raise InternalServerError


@router.put("/{appointment_id}")
async def update_appointment(config: Config, appointment_id: str, appointment: AppointmentModel):
    try:
        p_appointment = await fetch_appointment(config, appointment_id)
        if not p_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appointment with ID {appointment_id} does not exist")
        return await modify_appointment(config, appointment)
    except ServiceError:
        raise InternalServerError


@router.delete("/{appointment_id}")
async def delete_appointment(config: Config, user_id: str):
    try:
        await remove_appointment(config, user_id)
        return {"message": "Appointment deleted successfully"}
    except ServiceError:
        raise InternalServerError




