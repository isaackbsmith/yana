import uuid
import pendulum

from yana.data.queries.adherence import (
    insert_adherence_slot,
    select_adherence_schedule_slot,
    select_adherence_slot,
    select_all_adherence_slots,
    select_next_adherence_slot,
    select_overall_adherence_rate,
    select_slot_by_reminder_status,
    update_adherence_status
)
from yana.data.schemas.adherence import AdherenceRateSchema, AdherenceSlotSchema, FullAdherenceSlotSchema, NewAdherenceSlotSchema
from yana.domain.exceptions import QueryError, ServiceError
from yana.domain.models.adherence import AdherenceRateModel, AdherenceSlotModel, AdherenceStatus, FullAdherenceSlotModel, ReminderStatus
from yana.domain.models.schedule import NewScheduleModel
from yana.domain.types import YANAConfig
from yana.domain.logger import api_logger
from yana.utils.datetime import to_unix_time_ts


async def fetch_adherence_slot(
    config: YANAConfig, slot_id: str
) -> AdherenceSlotModel | None:
    try:
        result = await select_adherence_slot(config, slot_id)
        if result and isinstance(result, AdherenceSlotSchema):
            slot = AdherenceSlotModel(**result.model_dump())
            return slot
        return None
    except QueryError:
        api_logger.error("An error occurred fetching adherence slot")
        raise ServiceError("Adherence Service Error")


async def fetch_next_adherence_slot(
    config: YANAConfig
) -> FullAdherenceSlotModel | None:
    try:
        current_datetime = pendulum.now().int_timestamp
        result = await select_next_adherence_slot(config, current_datetime)
        if result and isinstance(result, FullAdherenceSlotSchema):
            return FullAdherenceSlotModel(**result.model_dump())
        return None
    except QueryError:
        api_logger.error("An error occurred fetching next adherence slot")
        raise ServiceError("Adherence Service Error")

async def fetch_slot_by_reminder_status(
    config: YANAConfig,
    status: ReminderStatus
) -> FullAdherenceSlotModel | None:
    try:
        current_datetime = pendulum.now().int_timestamp
        result = await select_slot_by_reminder_status(config, current_datetime, status.value)
        if result and isinstance(result, FullAdherenceSlotSchema):
            return FullAdherenceSlotModel(**result.model_dump())
        return None
    except QueryError:
        api_logger.error("An error occurred fetching adherence slot")
        raise ServiceError("Adherence Service Error")

async def fetch_adherence_slots_for_schedule(
    config: YANAConfig, schedule_id: str
) -> list[FullAdherenceSlotModel] | list:
    try:
        result = await select_adherence_schedule_slot(config, schedule_id)
        if result and isinstance(result, list) and len(result) > 0:
            slots = list(
                map(lambda x: FullAdherenceSlotModel(**x.model_dump()), result)
            )
            return slots
        return []
    except QueryError:
        api_logger.error("An error occurred fetching adherence slots for schedule")
        raise ServiceError("Adherence Service Error")

async def fetch_all_adherence_slots(
    config: YANAConfig
) -> list[AdherenceSlotModel] | list:
    try:
        result = await select_all_adherence_slots(config)
        if result and isinstance(result, list) and len(result) > 0:
            slots = list(
                map(lambda x: AdherenceSlotModel(**x.model_dump()), result)
            )
            return slots
        return []
    except QueryError:
        api_logger.error("An error occurred fetching adherence slots")
        raise ServiceError("Adherence Service Error")

async def create_adherence_slot(config: YANAConfig, schedule: NewScheduleModel, schedule_id: str):
    """
    Create adherence slots for a given schedule

    arguments:
        schedule: The schedule model
    """
    id = str(uuid.uuid4())

    # Compose schedule datetime object
    schedule_datetime = schedule.begin_date.add(seconds=to_unix_time_ts(schedule.begin_time))

    # Shift the time by the user defined offset
    # slot_datetime = schedule_datetime.subtract(minutes=schedule.reminder_offset)
    slot_datetime = schedule_datetime

    slot = NewAdherenceSlotSchema(
        id=id,
        datetime=slot_datetime.int_timestamp,
        schedule_id=schedule_id
    )
    await insert_adherence_slot(config, slot)


async def set_adherence_status(config: YANAConfig, slot: FullAdherenceSlotModel, status: AdherenceStatus) -> None:
    await update_adherence_status(config, slot.id, status.value)


async def fetch_adherence_rate(config: YANAConfig) -> AdherenceRateModel | None:
    try:
        result = await select_overall_adherence_rate(config)
        if result and isinstance(result, AdherenceRateSchema):
            slot = AdherenceRateModel(**result.model_dump())
            return slot
        return None
    except QueryError:
        api_logger.error("An error occurred fetching adherence rate")
        raise ServiceError("Adherence Service Error")
