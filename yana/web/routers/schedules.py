from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from yana.domain.exceptions import ServiceError
from yana.domain.models.schedule import NewScheduleModel, ScheduleModel
from yana.service.schedules import create_schedule, fetch_schedule, modify_schedule, remove_schedule
from yana.web.exceptions import InternalServerError
from yana.web.types import Config


router = APIRouter(
    prefix="/schedules",
    tags=["schedules"]
)


@router.get("/")
async def home() -> str:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This endpoint is not allowed")


@router.post("/new")
async def new_schedule(config: Config, schedule: NewScheduleModel):
    try:
        await create_schedule(config, schedule)
    except ServiceError:
        raise InternalServerError


@router.get("/{schedule_id}")
async def get_schedule(config: Config, medication_name: str):
    try:
        medication = await fetch_schedule(config, medication_name)
        if not medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Schedule does not exist")
        return medication
    except ServiceError:
        raise InternalServerError


@router.put("/{schedule_id}")
async def update_schedule(config: Config, schedule_id: str, schedule: ScheduleModel):
    try:
        p_medication = await fetch_schedule(config, schedule_id)
        if not p_medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Schedule with ID {schedule_id} does not exist")
        return await modify_schedule(config, schedule)
    except ServiceError:
        raise InternalServerError


@router.delete("/{schedule_id}")
async def delete_schedule(config: Config, medication_id: str):
    try:
        await remove_schedule(config, medication_id)
        return {"message": "Schedule deleted successfully"}
    except ServiceError:
        raise InternalServerError


