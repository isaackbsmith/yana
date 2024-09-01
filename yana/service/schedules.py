import uuid
from typing import cast
from yana.data.queries.schedules import delete_schedule, insert_schedule, insert_schedule_dow, select_schedule, update_schedule
from yana.data.schemas.schedule import ScheduleSchema
from yana.domain.exceptions import QueryError, ServiceError
from yana.domain.models.schedule import NewScheduleModel, Repeated, RepeatedMonthlyOn, RepeatedUntil, ScheduleModel
from yana.domain.types import YANAConfig
from yana.domain.logger import api_logger
from yana.utils.datetime import from_ts


async def fetch_schedule(config: YANAConfig, id: str) -> ScheduleModel | None:
    try:
        result = await select_schedule(config, id)
        if result and isinstance(result, ScheduleSchema):
            schedule = ScheduleModel(
                id = result.id,
                begin_date = from_ts(result.begin_date),
                end_date = from_ts(result.end_date),
                begin_time = from_ts(result.begin_time),
                end_time = from_ts(result.end_time) if result.end_time else None,
                schedule_type = result.schedule_type,
                repeated = Repeated.try_from_str(result.repeated) if result.repeated else None,
                repetition_step = result.repetition_step,
                repeated_monthly_on = RepeatedMonthlyOn.try_from_str(result.repeated_monthly_on) if result.repeated_monthly_on else None,
                repeated_until = RepeatedUntil.try_from_str(result.repeated_until) if result.repeated_until else None,
                repeated_until_date = from_ts(result.repeated_until_date) if result.repeated_until_date else None,
                repeated_reps = result.repeated_reps,
                user_id = result.user_id,
                medication_id = result.medication_id,
                appointment_id = result.appointment_id
            )
            return schedule
        return None
    except QueryError:
        api_logger.error("An error occurred fetching schedule")
        raise ServiceError("Schedule Service Error")


async def create_schedule(config: YANAConfig, schedule: NewScheduleModel) -> None:

    id = str(uuid.uuid4())

    new_schedule = ScheduleSchema(
        id = id,
        begin_date = schedule.begin_date.int_timestamp,
        end_date = schedule.end_date.int_timestamp,
        begin_time = schedule.begin_time.int_timestamp,
        end_time = schedule.end_time.int_timestamp if schedule.end_time else None,
        schedule_type = schedule.schedule_type,
        repeated = schedule.repeated.value if schedule.repeated else None,
        repetition_step = schedule.repetition_step,
        repeated_monthly_on = schedule.repeated_monthly_on.value if schedule.repeated_monthly_on else None,
        repeated_until = schedule.repeated_until.value if schedule.repeated_until else None,
        repeated_until_date = schedule.repeated_until_date.int_timestamp if schedule.repeated_until_date else None,
        repeated_reps = schedule.repeated_reps,
        user_id = schedule.user_id,
        medication_id = schedule.medication_id,
        appointment_id = schedule.appointment_id
    )

    try:
        await insert_schedule(config, new_schedule)
        # If schedule is a weekly repeated schedule, create a dow mapping
        if schedule.repeated is Repeated.WEEKLY:
            await insert_schedule_dow(config, id, schedule.days_of_week)
    except QueryError:
        api_logger.error("An error occurred creating schedule")
        raise ServiceError("Schedule Service Error")


async def modify_schedule(config: YANAConfig, schedule: ScheduleModel) -> ScheduleModel:

    updated_schedule = ScheduleSchema(
        id = schedule.id,
        begin_date = schedule.begin_date.int_timestamp,
        end_date = schedule.end_date.int_timestamp,
        begin_time = schedule.begin_time.int_timestamp,
        end_time = schedule.end_time.int_timestamp if schedule.end_time else None,
        schedule_type = schedule.schedule_type,
        repeated = schedule.repeated.value if schedule.repeated else None,
        repetition_step = schedule.repetition_step,
        repeated_monthly_on = schedule.repeated_monthly_on.value if schedule.repeated_monthly_on else None,
        repeated_until = schedule.repeated_until.value if schedule.repeated_until else None,
        repeated_until_date = schedule.repeated_until_date.int_timestamp if schedule.repeated_until_date else None,
        repeated_reps = schedule.repeated_reps,
        user_id = schedule.user_id,
        medication_id = schedule.medication_id,
        appointment_id = schedule.appointment_id
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




