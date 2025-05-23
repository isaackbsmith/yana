from typing import cast
import uuid
from yana.data.queries.appointments import (
    delete_appointment,
    insert_appointment,
    select_all_appointment,
    select_appointment,
    update_appointment,
)
from yana.data.schemas.appointment import AppointmentSchema
from yana.domain.exceptions import QueryError, ServiceError
from yana.domain.models.appointment import BaseAppointmentModel, FullAppointmentModel
from yana.domain.types import YANAConfig
from yana.domain.logger import api_logger


async def fetch_appointment(
    config: YANAConfig, appointment_id: str
) -> FullAppointmentModel | None:
    try:
        result = await select_appointment(config, appointment_id)
        if result and isinstance(result, AppointmentSchema):
            appointment = FullAppointmentModel(**result.model_dump())
            return appointment
        return None
    except QueryError:
        api_logger.error("An error occurred fetching appointment")
        raise ServiceError("Appointment Service Error")


async def create_appointment(config: YANAConfig, appointment: BaseAppointmentModel) -> FullAppointmentModel:
    id = str(uuid.uuid4())

    new_appointment = AppointmentSchema(**appointment.model_dump(), id=id)

    try:
        await insert_appointment(config, new_appointment)
        return cast(FullAppointmentModel, await fetch_appointment(config, id))
    except QueryError:
        api_logger.error("An error occurred creating appointment")
        raise ServiceError("Appointment Service Error")

async def fetch_all_appointments(config: YANAConfig):
    try:
        result = await select_all_appointment(config)
        if result and isinstance(result, list) and len(result) > 0:
            medications = list(
                map(lambda x: FullAppointmentModel(**x.model_dump()), result)
            )
            return medications
        return []
    except QueryError:
        api_logger.error("An error occurred fetching appointments")
        raise ServiceError("Medication Service Error")

async def modify_appointment(
    config: YANAConfig, appointment: FullAppointmentModel
) -> FullAppointmentModel:
    updated_appointment = AppointmentSchema(**appointment.model_dump())

    try:
        await update_appointment(config, updated_appointment)
        return cast(
            FullAppointmentModel, await fetch_appointment(config, updated_appointment.id)
        )
    except QueryError:
        api_logger.error("An error occurred updating appointment")
        raise ServiceError("Appointment Service Error")


async def remove_appointment(config: YANAConfig, appointment_id: str) -> None:
    try:
        await delete_appointment(config, appointment_id)
    except QueryError:
        api_logger.error("An error occurred deleting appointment")
        raise ServiceError("Appointment Service Error")
