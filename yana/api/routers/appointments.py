from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from yana.domain.exceptions import ServiceError
from yana.domain.models.appointment import BaseAppointmentModel, FullAppointmentModel
from yana.service.appointments import (
    create_appointment,
    fetch_all_appointments,
    fetch_appointment,
    modify_appointment,
    remove_appointment,
)
from yana.api.exceptions import InternalServerError
from yana.api.types import Config


router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/")
async def home() -> str:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="This endpoint is not allowed"
    )

@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=FullAppointmentModel)
async def new_appointment(config: Config, appointment: BaseAppointmentModel):
    try:
        return await create_appointment(config, appointment)
    except ServiceError:
        raise InternalServerError

@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[FullAppointmentModel])
async def get_all_appointments(config: Config) -> list[FullAppointmentModel] | list:
    try:
        return await fetch_all_appointments(config)
    except ServiceError:
        raise InternalServerError

@router.get("/{appointment_id}", status_code=status.HTTP_200_OK, response_model=FullAppointmentModel)
async def get_appointment(config: Config, appointment_id: str):
    try:
        user = await fetch_appointment(config, appointment_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment does not exist",
            )
        return user
    except ServiceError:
        raise InternalServerError

@router.put("/{appointment_id}", status_code=status.HTTP_201_CREATED, response_model=FullAppointmentModel)
async def update_appointment(
    config: Config, appointment_id: str, appointment: FullAppointmentModel
):
    try:
        p_appointment = await fetch_appointment(config, appointment_id)
        if not p_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appointment with ID {appointment_id} does not exist",
            )
        return await modify_appointment(config, appointment)
    except ServiceError:
        raise InternalServerError


@router.delete("/{appointment_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_appointment(config: Config, user_id: str):
    try:
        await remove_appointment(config, user_id)
        return {"message": "Appointment deleted successfully"}
    except ServiceError:
        raise InternalServerError
