from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from yana.domain.exceptions import ServiceError
from yana.api.exceptions import InternalServerError
from yana.api.types import Config
from yana.domain.models.adherence import AdherenceSlotModel, FullAdherenceSlotModel
from yana.service.adherence import fetch_adherence_slot, fetch_adherence_slots_for_schedule, fetch_all_adherence_slots, fetch_next_adherence_slot


router = APIRouter(prefix="/adherence", tags=["adherence"])


@router.get("/")
async def home() -> str:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="This endpoint is not allowed"
    )


@router.get("/next", status_code=status.HTTP_200_OK, response_model=FullAdherenceSlotModel)
async def get_next_adherence_slot(config: Config):
    try:
        slot = await fetch_next_adherence_slot(config)
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There are no adherence slots for today"
            )
        return slot
    except ServiceError:
        raise InternalServerError

@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[AdherenceSlotModel] | list)
async def get_all_adherence_slots(config: Config):
    try:
        return await fetch_all_adherence_slots(config)
    except ServiceError:
        raise InternalServerError

@router.get("/schedule/{schedule_id}", status_code=status.HTTP_200_OK, response_model=list[FullAdherenceSlotModel] | list)
async def get_adherence_slots_for_schedule(config: Config, schedule_id: str):
    try:
        return await fetch_adherence_slots_for_schedule(config, schedule_id)
    except ServiceError:
        raise InternalServerError

@router.get("/{slot_id}", status_code=status.HTTP_200_OK, response_model=FullAdherenceSlotModel)
async def get_adherence_slot(config: Config, slot_id: str):
    try:
        slot = await fetch_adherence_slot(config, slot_id)
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Adherence slot does not exist"
            )
        return slot
    except ServiceError:
        raise InternalServerError


# The user can:
#   get all adherence for the day, week, month, year
#   get current adherence slot



