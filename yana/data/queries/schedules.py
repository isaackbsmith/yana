from yana.data.database import run_query
from yana.data.schemas.appointment import AppointmentSchema
from yana.data.schemas.medication import MedicationSchema
from yana.data.schemas.schedule import NewScheduleSchema, ScheduleMedicationSchema, ScheduleSchema
from yana.domain.exceptions import DatabaseError, QueryError
from yana.domain.models import DOW
from yana.domain.types import YANAConfig


async def select_schedule(config: YANAConfig, id: str):
    sql = """
        SELECT
            sched.id,
            sched.begin_date,
            sched.end_date,
            sched.begin_time,
            sched.end_time,
            sched.schedule_type,
            sched.repeated,
            sched.repetition_step,
            sched.repeated_monthly_on,
            sched.repeated_until,
            sched.repeated_until_date,
            sched.repeated_reps,
            med.brand_name AS medication,
            app.reason AS appointment
        FROM schedules AS sched
        LEFT JOIN medications AS med ON sched.medication_id = med.id
        LEFT JOIN appointments AS app ON sched.appointment_id = app.id
        WHERE sched.id = :id AND sched.medication_id IS NOT NULL OR sched.appointment_id IS NOT NULl
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"id": id},
            factory=ScheduleSchema,
            pragma="one",
        )
    except DatabaseError:
        raise QueryError("Error selecting schedule")

async def select_all_schedules(config: YANAConfig):
    sql = """
        SELECT
            sched.id,
            sched.begin_date,
            sched.end_date,
            sched.begin_time,
            sched.end_time,
            sched.schedule_type,
            sched.repeated,
            sched.repetition_step,
            sched.repeated_monthly_on,
            sched.repeated_until,
            sched.repeated_until_date,
            sched.repeated_reps,
            med.brand_name AS medication,
            app.reason AS appointment
        FROM schedules AS sched
        LEFT JOIN medications AS med ON sched.medication_id = med.id
        LEFT JOIN appointments AS app ON sched.appointment_id = app.id
        WHERE sched.medication_id IS NOT NULL OR sched.appointment_id IS NOT NULl
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            factory=ScheduleSchema,
            pragma="all",
        )
    except DatabaseError:
        raise QueryError("Error selecting schedules")

async def select_schedule_medication(config: YANAConfig, schedule_id: str):
    sql = """
        SELECT
            med.id,
            med.generic_name,
            med.brand_name,
            med.description,
            med.strength,
            med.dosage,
            dosage.name AS dosage_form,
            route.name AS medication_route
        FROM schedules AS sched
        INNER JOIN medications AS med ON sched.medication_id = med.id
        INNER JOIN dosage_forms AS dosage ON med.dosage_form_id = dosage.id
        INNER JOIN medication_routes AS route ON med.medication_route_id = route.id
        WHERE sched.id = :schedule_id
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"schedule_id": schedule_id},
            factory=MedicationSchema,
            pragma="one",
        )
    except DatabaseError:
        raise QueryError("Error selecting schedule medication")

async def select_schedule_appointment(config: YANAConfig, schedule_id: str):
    sql = """
        SELECT
        app.id,
        app.reason,
        app.location
        FROM schedules AS sched
        INNER JOIN appointments AS app ON sched.appointment_id = app.id
        WHERE sched.id = :schedule_id
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"schedule_id": schedule_id},
            factory=AppointmentSchema,
            pragma="one",
        )
    except DatabaseError:
        raise QueryError("Error selecting schedule appointment")


async def insert_schedule(config: YANAConfig, schedule: NewScheduleSchema):
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
            :medication_id,
            :appointment_id
        );
        """
    try:
        return await run_query(
            config=config, sql=sql, params=schedule.model_dump(), factory=ScheduleSchema
        )
    except DatabaseError:
        raise QueryError("Error inserting new schedule")


async def update_schedule(config: YANAConfig, schedule: NewScheduleSchema):
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
            medication_id = :medication_id,
            appointment_id = :appointment_id
        WHERE id = :id;
        """
    try:
        return await run_query(
            config=config, sql=sql, params=schedule.model_dump(), factory=ScheduleSchema
        )
    except DatabaseError:
        raise QueryError("Error updating schedule")


async def delete_schedule(config: YANAConfig, id: str):
    sql = """
        DELETE FROM schedules WHERE id = :id;
        """
    try:
        return await run_query(
            config=config, sql=sql, params={"id": id}, factory=ScheduleSchema
        )
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
                factory=ScheduleSchema,
            )
    except DatabaseError:
        raise QueryError("Error inserting new schedule day of week")

