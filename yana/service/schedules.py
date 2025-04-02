import uuid
from typing import cast
from yana.data.queries.schedules import (
    delete_schedule,
    insert_schedule,
    insert_schedule_dow,
    select_all_schedules,
    select_schedule,
    select_schedule_appointment,
    select_schedule_medication,
    update_schedule,
)
from yana.data.schemas.medication import MedicationSchema
from yana.data.schemas.schedule import NewScheduleSchema, ScheduleSchema
from yana.domain.exceptions import QueryError, ServiceError
from yana.domain.models.appointment import FullAppointmentModel
from yana.domain.models.medication import MedicationModel
from yana.domain.models.schedule import (
    NewScheduleModel,
    Repeated,
    RepeatedMonthlyOn,
    RepeatedUntil,
    ScheduleModel,
)
from yana.domain.types import YANAConfig
from yana.domain.logger import api_logger
from yana.service.adherence import create_adherence_slot
from yana.utils.datetime import date_from_ts, time_from_secs, to_unix_date_ts, to_unix_time_ts


def _to_schedule_model(result: ScheduleSchema) -> ScheduleModel:
    schedule = ScheduleModel(
        id=result.id,
        begin_date=date_from_ts(result.begin_date),
        end_date=date_from_ts(result.end_date) if result.end_date else None,
        begin_time=time_from_secs(result.begin_time),
        end_time=time_from_secs(result.end_time) if result.end_time else None,
        schedule_type=result.schedule_type,
        repeated=Repeated.try_from_str(result.repeated)
        if result.repeated
        else None,
        repetition_step=result.repetition_step,
        repeated_monthly_on=RepeatedMonthlyOn.try_from_str(
            result.repeated_monthly_on
        )
        if result.repeated_monthly_on
        else None,
        repeated_until=RepeatedUntil.try_from_str(result.repeated_until)
        if result.repeated_until
        else None,
        repeated_until_date=date_from_ts(result.repeated_until_date)
        if result.repeated_until_date
        else None,
        repeated_reps=result.repeated_reps,
        medication=result.medication,
        appointment=result.appointment,
    )
    return schedule


async def fetch_schedule(config: YANAConfig, id: str) -> ScheduleModel | None:
    try:
        result = await select_schedule(config, id)
        if result and isinstance(result, ScheduleSchema):
            return _to_schedule_model(result)
        return None
    except QueryError:
        api_logger.error("An error occurred fetching schedule")
        raise ServiceError("Schedule Service Error")


async def fetch_all_schedules(config: YANAConfig):
    try:
        result = await select_all_schedules(config)
        if result and isinstance(result, list) and len(result) > 0:
            schedules = list(
                map(lambda x: _to_schedule_model(x), result)
            )
            return schedules
        return []
    except QueryError:
        api_logger.error("An error occurred fetching schedules")
        raise ServiceError("Medication Service Error")

async def fetch_schedule_medication(config: YANAConfig, id: str) -> MedicationModel | None:
    try:
        result = await select_schedule_medication(config, id)
        if result and isinstance(result, MedicationSchema):
            medication = MedicationModel(**result.model_dump())
            return medication
        return None
    except QueryError:
        api_logger.error("An error occurred fetching schedule medication")
        raise ServiceError("Schedule Service Error")

async def fetch_schedule_appointment(config: YANAConfig, id: str) -> FullAppointmentModel | None:
    try:
        result = await select_schedule_appointment(config, id)
        if result and isinstance(result, MedicationSchema):
            appointment = FullAppointmentModel(**result.model_dump())
            return appointment
        return None
    except QueryError:
        api_logger.error("An error occurred fetching schedule appointment")
        raise ServiceError("Schedule Service Error")

async def create_schedule(config: YANAConfig, schedule: NewScheduleModel) -> ScheduleModel:
    id = str(uuid.uuid4())

    # Check if new schedule overlaps with existing ones
    new_schedule = NewScheduleSchema(
        id=id,
        begin_date=to_unix_date_ts(schedule.begin_date),
        end_date=to_unix_date_ts(schedule.end_date) if schedule.end_date else None,
        begin_time=to_unix_time_ts(schedule.begin_time),
        end_time=to_unix_time_ts(schedule.end_time) if schedule.end_time else None,
        schedule_type=schedule.schedule_type,
        repeated=schedule.repeated.value if schedule.repeated else None,
        repetition_step=schedule.repetition_step,
        repeated_monthly_on=schedule.repeated_monthly_on.value
        if schedule.repeated_monthly_on
        else None,
        repeated_until=schedule.repeated_until.value
        if schedule.repeated_until
        else None,
        repeated_until_date=schedule.repeated_until_date.int_timestamp
        if schedule.repeated_until_date
        else None,
        repeated_reps=schedule.repeated_reps,
        medication_id=schedule.medication_id,
        appointment_id=schedule.appointment_id,
    )

    try:
        await insert_schedule(config, new_schedule)
        # If schedule is a weekly repeated schedule, create a day-of-the-week mapping
        if schedule.repeated is Repeated.WEEKLY and len(schedule.days_of_week) > 0:
            await insert_schedule_dow(config, id, schedule.days_of_week)
        # Create the adherence slots here
        api_logger.info(f"Creating Adherence Slot for Schedule: {id}")
        await create_adherence_slot(config, schedule, id)
        api_logger.info(f"Finished Creating Adherence Slot for Schedule: {id}")
        return cast(ScheduleModel, await fetch_schedule(config, new_schedule.id))
    except QueryError:
        api_logger.error("An error occurred creating schedule")
        raise ServiceError("Schedule Service Error")

async def modify_schedule(config: YANAConfig, id: str, schedule: NewScheduleModel) -> ScheduleModel:
    updated_schedule = NewScheduleSchema(
        id=id,
        begin_date=to_unix_date_ts(schedule.begin_date),
        end_date=to_unix_date_ts(schedule.end_date) if schedule.end_date else None,
        begin_time=to_unix_time_ts(schedule.begin_time),
        end_time=to_unix_time_ts(schedule.end_time) if schedule.end_time else None,
        schedule_type=schedule.schedule_type,
        repeated=schedule.repeated.value if schedule.repeated else None,
        repetition_step=schedule.repetition_step,
        repeated_monthly_on=schedule.repeated_monthly_on.value
        if schedule.repeated_monthly_on
        else None,
        repeated_until=schedule.repeated_until.value
        if schedule.repeated_until
        else None,
        repeated_until_date=to_unix_date_ts(schedule.repeated_until_date)
        if schedule.repeated_until_date
        else None,
        repeated_reps=schedule.repeated_reps,
        medication_id=schedule.medication_id,
        appointment_id=schedule.appointment_id,
    )

    try:
        await update_schedule(config, updated_schedule)
        return cast(ScheduleModel, await fetch_schedule(config, updated_schedule.id))
    except QueryError:
        api_logger.error("An error occurred updating schedule")
        raise ServiceError("Schedule Service Error")


async def remove_schedule(config: YANAConfig, id: str) -> None:
    try:
        await delete_schedule(config, id)
    except QueryError:
        api_logger.error("An error occurred deleting schedule")
        raise ServiceError("Schedule Service Error")
