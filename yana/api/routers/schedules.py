from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from yana.domain.exceptions import ServiceError
from yana.domain.models.schedule import NewScheduleModel, ScheduleModel
from yana.service.schedules import (
    create_schedule,
    fetch_all_schedules,
    fetch_schedule,
    modify_schedule,
    remove_schedule,
)
from yana.api.exceptions import InternalServerError
from yana.api.types import Config


router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.get("/")
async def home() -> str:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="This endpoint is not allowed"
    )


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=ScheduleModel)
async def new_schedule(config: Config, schedule: NewScheduleModel):
    try:
        return await create_schedule(config, schedule)
    except ServiceError:
        raise InternalServerError

@router.get("/all")
async def get_all_schedules(config: Config) -> list[ScheduleModel] | list:
    try:
        return await fetch_all_schedules(config)
    except ServiceError:
        raise InternalServerError

@router.get("/{schedule_id}", status_code=status.HTTP_200_OK, response_model=ScheduleModel)
async def get_schedule(config: Config, schedule_id: str):
    try:
        schedule = await fetch_schedule(config, schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Schedule does not exist"
            )
        return schedule
    except ServiceError:
        raise InternalServerError


@router.put("/{schedule_id}", status_code=status.HTTP_201_CREATED, response_model=ScheduleModel)
async def update_schedule(config: Config, schedule_id: str, schedule: NewScheduleModel):
    try:
        p_schedule = await fetch_schedule(config, schedule_id)
        if not p_schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Schedule does not exist",
            )
        return await modify_schedule(config, schedule_id, schedule)
    except ServiceError:
        raise InternalServerError


@router.delete("/{schedule_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_schedule(config: Config, schedule_id: str):
    try:
        schedule = await fetch_schedule(config, schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Schedule does not exist"
            )
        await remove_schedule(config, schedule_id)
        return {"message": "Schedule deleted successfully"}
    except ServiceError:
        raise InternalServerError
