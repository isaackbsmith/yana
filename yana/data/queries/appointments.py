from yana.data.database import run_query
from yana.data.schemas.appointment import AppointmentSchema
from yana.domain.exceptions import DatabaseError, QueryError
from yana.domain.types import YANAConfig


async def select_appointment(config: YANAConfig, appointment_id: str):
    sql = """
        SELECT
            id,
            reason,
            location
        FROM appointments
        WHERE id = :id
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"id": appointment_id},
            factory=AppointmentSchema,
            pragma="one",
        )
    except DatabaseError:
        raise QueryError("Error selecting new appointment")

async def select_all_appointment(config: YANAConfig):
    sql = """
        SELECT
            id,
            reason,
            location
        FROM appointments
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            factory=AppointmentSchema,
            pragma="all",
        )
    except DatabaseError:
        raise QueryError("Error selecting appointments")

async def insert_appointment(config: YANAConfig, appointment: AppointmentSchema):
    sql = """
        INSERT INTO appointments (
            id,
            reason,
            location
        ) VALUES (
            :id,
            :reason,
            :location
        );
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params=appointment.model_dump(),
            factory=AppointmentSchema,
        )
    except DatabaseError:
        raise QueryError("Error inserting new appointment")


async def update_appointment(config: YANAConfig, user: AppointmentSchema):
    sql = """
        UPDATE appointments
            reason = :reason,
            location = :location
        SET
        WHERE id = :id;
        """
    try:
        return await run_query(
            config=config, sql=sql, params=user.model_dump(), factory=AppointmentSchema
        )
    except DatabaseError:
        raise QueryError("Error updating appointment")


async def delete_appointment(config: YANAConfig, appointment_id: str):
    sql = """
        DELETE FROM appointments WHERE id = :id;
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"id": appointment_id},
            factory=AppointmentSchema,
        )
    except DatabaseError:
        raise QueryError("Error deleting appointment")
