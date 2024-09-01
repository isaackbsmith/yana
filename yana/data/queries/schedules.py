from yana.data.database import run_query
from yana.data.schemas.schedule import ScheduleSchema
from yana.domain.exceptions import DatabaseError, QueryError
from yana.domain.models import DOW
from yana.domain.types import YANAConfig


async def select_schedule(config: YANAConfig, id: str):
    sql = """
        SELECT
            id,
            begin_date,
            end_date,
            begin_time,
            end_time,
            schedule_type,
            repeated,
            repetition_step,
            repeated_monthly_on,
            repeated_until,
            repeated_until_date,
            repeated_reps,
            user_id,
            medication_id,
            appointment_id
        FROM schedules
        WHERE id = :id
    """
    try:
        return await run_query(config=config,
                                 sql=sql,
                                 params={"id": id},
                                 factory=ScheduleSchema,
                                 pragma="one")
    except DatabaseError:
        raise QueryError("Error selecting schedule")


async def insert_schedule(config: YANAConfig, schedule: ScheduleSchema):
    sql = """
        INSERT INTO schedules (
            id,
            begin_date,
            end_date,
            begin_time,
            end_time,
            schedule_type,
            repeated,
            repetition_step,
            repeated_monthly_on,
            repeated_until,
            repeated_until_date,
            repeated_reps,
            user_id,
            medication_id,
            appointment_id
        ) VALUES (
            :id,
            :begin_date,
            :end_date,
            :begin_time,
            :end_time,
            :schedule_type,
            :repeated,
            :repetition_step,
            :repeated_monthly_on,
            :repeated_until,
            :repeated_until_date,
            :repeated_reps,
            :user_id,
            :medication_id,
            :appointment_id
        );
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params=schedule.model_dump(),
            factory=ScheduleSchema)
    except DatabaseError:
        raise QueryError("Error inserting new schedule")


async def update_schedule(config: YANAConfig, schedule: ScheduleSchema):
    sql = """
        UPDATE schedules
        SET
            begin_date = :begin_date,
            end_date = :end_date,
            begin_time = :begin_time,
            end_time = :end_time,
            schedule_type = :schedule_type,
            repeated = :repeated,
            repetition_step = :repitition_step,
            repeated_monthly_on = :repeated_monthly_on,
            repeated_until = :repeated_until,
            repeated_until_date = :repeated_until_date,
            repeated_reps = :repeated_reps,
            user_id = :user_id,
            medication_id = :medication_id,
            appointment_id = :appointment_id
        WHERE id = :id;
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params=schedule.model_dump(),
            factory=ScheduleSchema)
    except DatabaseError:
        raise QueryError("Error updating schedule")


async def delete_schedule(config: YANAConfig, id: str):
    sql = """
        DELETE FROM schedules WHERE id = :id;
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"id": id},
            factory=ScheduleSchema)
    except DatabaseError:
        raise QueryError("Error deleting schedule")


async def insert_schedule_dow(config: YANAConfig, schedule_id: str, days: list[DOW]):
    sql = """
        INSERT INTO schedules_dows (
            schedule_id,
            day_of_week
        ) VALUES (
            :schedule_id,
            :dow
        );
        """
    try:
        for dow in days:
            await run_query(
                config=config,
                sql=sql,
                params={"schedule_id": schedule_id, "dow": dow.value},
                factory=ScheduleSchema)
    except DatabaseError:
        raise QueryError("Error inserting new schedule day of week")
